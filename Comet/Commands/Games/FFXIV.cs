using Microsoft.Extensions.Configuration;
using NetCord;
using NetCord.Rest;
using NetCord.Services;
using NetCord.Services.ApplicationCommands;
using System.Text.Encodings.Web;
using System.Text.Json;

namespace Comet.Commands.Games;

[SlashCommand("ff", "Final Fantasy XIV commands")]
public class FFXIV : ApplicationCommandModule<ApplicationCommandContext>
{
    [SubSlashCommand("convert", "Convert item.json file from id -> name to name -> id")] 
    public async Task<string> Convert() {      
        var inputPath = Path.Combine("Resources", "items.json");
        var outputPath = Path.Combine("Resources", "items-en.json");
        if (!File.Exists(inputPath) || File.Exists(outputPath)) return "items.json not found or items-en.json already exist"; 
        var json = await File.ReadAllTextAsync(inputPath); 
        var items = JsonSerializer.Deserialize< Dictionary<string, Dictionary<string, string>> >(json); 
        if (items == null) return "Failed to parse items.json."; 
        var converted = new Dictionary<string, int>( StringComparer.OrdinalIgnoreCase ); 
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
    public string PriceCheck(string item)
    {
        var json = await File.ReadAllTextAsync(Path.Combine(AppContext.BaseDirectory, "Resources", "items-en.json"));
        if (json == null)
        {
            return "Resource not found, have you convert it yet?";
        }

        var items = JsonSerializer.Deserialize<Dictionary<string, int>>(json);
        if (items != null && items.TryGetValue(item, out var itemId))
        {
            return $"Item found: {itemId}";
        }
        else
        {
            return "Item not found";
        }
    }

}

