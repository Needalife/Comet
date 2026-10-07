using Comet.Services.FFXIV.Models;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Net.Http.Json;
using System.Text;

namespace Comet.Services.FFXIV;

public class Universalis
{
    private readonly IConfiguration _config;
    private readonly HttpClient _client;
    private readonly ILogger<Universalis> _logger;
    public Universalis(IConfiguration config, HttpClient client, ILogger<Universalis> logger)
    {
        _config = config;
        _client = client;
        _logger = logger;
    }

    public async Task<MarketBoardResponse> CheckMarketBoard(MarketBoardRequest request)
    {
        var query = new List<string>();
        if (!string.IsNullOrWhiteSpace(request.Listings)) query.Add($"listings={request.Listings}");
        if (!string.IsNullOrWhiteSpace(request.Entries)) query.Add($"entries={request.Entries}");
        if (!string.IsNullOrWhiteSpace(request.Fields)) query.Add($"fields={Uri.EscapeDataString(request.Fields)}");

        var url = $"{_config["APIs:Universalis"]}/{request.WorldDcRegion}/{request.ItemIds}";
        if (query.Count > 0)
        {
            url += "?" + string.Join("&", query);
        }

        var response = await _client.GetAsync(url);
        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<MarketBoardResponse>() ?? throw new InvalidOperationException("Universalis returned an empty response.");
    }

}

