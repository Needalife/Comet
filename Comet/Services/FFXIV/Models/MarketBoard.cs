using System;
using System.Collections.Generic;
using System.Text;

namespace Comet.Services.FFXIV.Models;


public class MarketBoardRequest
{
    public required string ItemIds { get; set; }
    public required string WorldDcRegion { get; set; }
    public string? Listings { get; set; }
    public string? Entries { get; set; }
    public string? Fields { get; set; }
}

public class MarketBoardResponse
{
    public List<Item> Listings { get; set; } = [];
    public List<SaleHistory> RecentHistory { get; set; } = [];
}

public class Item
{
    public long PricePerUnit { get; set; }
    public int Quantity { get; set; }
    public long Total { get; set; }
    public bool Hq { get; set; }
}

public class SaleHistory
{
    public bool Hq { get; set; }
    public long PricePerUnit { get; set; }
    public int Quantity { get; set; }
    public long Timestamp { get; set; }
    public long Total { get; set; }
}

