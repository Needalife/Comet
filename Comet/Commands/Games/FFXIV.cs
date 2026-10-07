using NetCord.Rest;
using NetCord.Services.ApplicationCommands;
using System.Text.Encodings.Web;
using System.Text.Json;
using Comet.Services.FFXIV;
using Comet.Services.FFXIV.Models;
using Comet.Utils;

namespace Comet.Commands.Games;

[SlashCommand("ff", "Final Fantasy XIV commands")]
public class FFXIV : BaseCommand
{
    private readonly string itemPath = Path.Combine("Resources", "items-en.json");
    private readonly Universalis _service;

    public FFXIV(Universalis universalis)
    {
        _service = universalis;
    }

    [SubSlashCommand("convert", "Convert item.json file from id -> name to name -> id")] 
    public async Task<string> Convert() {      
        var inputPath = Path.Combine("Resources", "items.json");
        var outputPath = itemPath;
        if (!File.Exists(inputPath) || File.Exists(outputPath)) return "items.json not found or items-en.json already exist"; 
        var json = await File.ReadAllTextAsync(inputPath); 
        var items = JsonSerializer.Deserialize< Dictionary<string, Dictionary<string, string>> >(json); 
        if (items == null) return "Failed to parse items.json."; 
        var converted = new Dictionary<string, int>(StringComparer.OrdinalIgnoreCase); 
        foreach (var item in items) { 
            if (!int.TryParse(item.Key, out var id)) continue; 
            if (!item.Value.TryGetValue("en", out var name)) continue; 
            if (string.IsNullOrWhiteSpace(name)) continue; 
            if (!converted.TryAdd(name, id)) { 
                Console.WriteLine( $"Duplicate item name: {name} ({converted[name]} / {id})" ); 
            } 
        }
        var outputJson = JsonSerializer.Serialize(
            converted,
            new JsonSerializerOptions
            {
                WriteIndented = true,
                Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping
            }
        );
        await File.WriteAllTextAsync(outputPath, outputJson);
        return $"Converted {converted.Count:N0} items to {outputPath}."; 
    }

    [SubSlashCommand("pc", "Price check an item")]
    public async Task PriceCheck(
        [SlashCommandParameter(Name = "item", Description = "Name of the item")] string item,
        [SlashCommandParameter(Name = "listings", Description = "The number of listing")] int nListings = 5,
        [SlashCommandParameter(Name = "entries", Description = "The number of entries")] int nEntries = 5,
        [SlashCommandParameter(Name = "wdr", Description = "The world, data center, or region")] string wdr = "Carbuncle")
    {
        var json = await File.ReadAllTextAsync(itemPath);       
        if (json == null)
        {
            await RespondError($"Fail to read file {itemPath}.");
        }

        var items = JsonSerializer.Deserialize<Dictionary<string, int>>(json);
        if (items != null)
        {
            items = new Dictionary<string, int>(
                items,
                StringComparer.OrdinalIgnoreCase
            );

            if (!items.TryGetValue(item, out int itemId))
            {
                await RespondError("Item not found.");
            }

            string fields = "listings.pricePerUnit,listings.quantity,listings.total,listings.hq,recentHistory.pricePerUnit,recentHistory.quantity,recentHistory.total,recentHistory.hq,recentHistory.timestamp";
            MarketBoardRequest request = new MarketBoardRequest
            {
                ItemIds = itemId.ToString(),
                WorldDcRegion = wdr,
                Listings = nListings.ToString(),
                Entries = nEntries.ToString(),
                Fields = fields
            };

            MarketBoardResponse response = await _service.CheckMarketBoard(request);
            var listings = string.Join(
                "\n",
                response.Listings.Select(x =>
                    $"{(x.Hq ? "HQ" : "NQ")} `{x.PricePerUnit:N0} gil × {x.Quantity} = {x.Total} gil`"
                )
            );
            var history = string.Join(
                "\n",
                response.RecentHistory.Select(x =>
                    $"{(x.Hq ? "HQ" : "NQ")} `{x.PricePerUnit:N0} gil × {x.Quantity} = {x.Total} gil` at <t:{x.Timestamp}:f>"
                )
            );

            var embed = new EmbedProperties
            {
                Title = item,
                Description = $"Market Board — {request.WorldDcRegion}",
                Color = Colors.Random(),

                Fields =
                [
                    new EmbedFieldProperties
                    {
                        Name = "Current Listings",
                        Value = string.IsNullOrEmpty(listings) ? "No listings found." : listings
                    },

                    new EmbedFieldProperties
                    {
                        Name = "Recent Sales",
                        Value = string.IsNullOrEmpty(history) ? "No recent sales." : history
                    }
                ]
            };

            await Respond(embed);
        }
        else
        {
            await RespondError("Can't deserialize item");
        }
    }

}

