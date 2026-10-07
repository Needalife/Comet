using NetCord;

namespace Comet.Utils;

public static class Colors
{
    // Semantic
    public static readonly Color Success = new(0x57F287);
    public static readonly Color Error = new(0xED4245);
    public static readonly Color Warning = new(0xF1C40F);
    public static readonly Color Info = new(0x5865F2);
    public static readonly Color Neutral = new(0x95A5A6);

    // Discord
    public static readonly Color DiscordBlurple = new(0x5865F2);
    public static readonly Color DiscordGreen = new(0x57F287);
    public static readonly Color DiscordRed = new(0xED4245);
    public static readonly Color DiscordYellow = new(0xFEE75C);
    public static readonly Color DiscordFuchsia = new(0xEB459E);

    // Reds
    public static readonly Color Red = new(0xFF4444);
    public static readonly Color LightRed = new(0xFF6B6B);
    public static readonly Color DarkRed = new(0xC0392B);
    public static readonly Color Crimson = new(0xDC143C);
    public static readonly Color DarkCrimson = new(0x8B0000);
    public static readonly Color Maroon = new(0x800000);

    // Oranges
    public static readonly Color Orange = new(0xE67E22);
    public static readonly Color LightOrange = new(0xF39C12);
    public static readonly Color DarkOrange = new(0xFF8C00);
    public static readonly Color BurntOrange = new(0xCC5500);

    // Yellows / Gold
    public static readonly Color Yellow = new(0xF1C40F);
    public static readonly Color LightYellow = new(0xFFD166);
    public static readonly Color Gold = new(0xFFD700);
    public static readonly Color Amber = new(0xFFC107);

    // Greens
    public static readonly Color Green = new(0x2ECC71);
    public static readonly Color LightGreen = new(0x57F287);
    public static readonly Color DarkGreen = new(0x27AE60);
    public static readonly Color Emerald = new(0x50C878);
    public static readonly Color ForestGreen = new(0x228B22);
    public static readonly Color Lime = new(0xA4DE02);

    // Cyans / Teals
    public static readonly Color Cyan = new(0x00BCD4);
    public static readonly Color LightCyan = new(0x4DD0E1);
    public static readonly Color Teal = new(0x1ABC9C);
    public static readonly Color DarkTeal = new(0x16A085);
    public static readonly Color Aqua = new(0x00FFFF);

    // Blues
    public static readonly Color Blue = new(0x3498DB);
    public static readonly Color LightBlue = new(0x5DADE2);
    public static readonly Color DarkBlue = new(0x2980B9);
    public static readonly Color Navy = new(0x000080);
    public static readonly Color SkyBlue = new(0x87CEEB);
    public static readonly Color BrightBlue = new(0x00A8FF);

    // Purples
    public static readonly Color Purple = new(0x9B59B6);
    public static readonly Color LightPurple = new(0xBB8FCE);
    public static readonly Color DarkPurple = new(0x8E44AD);
    public static readonly Color Violet = new(0x6C5CE7);
    public static readonly Color Indigo = new(0x4B0082);

    // Pinks
    public static readonly Color Pink = new(0xE91E63);
    public static readonly Color LightPink = new(0xFF69B4);
    public static readonly Color HotPink = new(0xFF1493);
    public static readonly Color Rose = new(0xD63384);
    public static readonly Color Magenta = new(0xFF00FF);

    // Grayscale
    public static readonly Color White = new(0xFFFFFF);
    public static readonly Color Silver = new(0xC0C0C0);
    public static readonly Color LightGray = new(0xD3D3D3);
    public static readonly Color Gray = new(0x95A5A6);
    public static readonly Color DarkGray = new(0x7F8C8D);
    public static readonly Color Slate = new(0x2C3E50);
    public static readonly Color DarkSlate = new(0x34495E);
    public static readonly Color AlmostBlack = new(0x1F1F1F);
    public static readonly Color Black = new(0x000000);


    // Special / FFXIV-ish
    public static readonly Color Gil = new(0xFFD700);
    public static readonly Color HQ = new(0xFFD700);
    public static readonly Color NQ = new(0x95A5A6);
    public static readonly Color Tank = new(0x3498DB);
    public static readonly Color Healer = new(0x57F287);
    public static readonly Color DPS = new(0xED4245);
    public static readonly Color Rare = new(0x9B59B6);
    public static readonly Color Legendary = new(0xFF8C00);

    // Random
    public static Color Random() => new(System.Random.Shared.Next(0x1000000));
}