using NetCord;
using NetCord.Gateway;
using NetCord.Logging;
using NetCord.Rest;
using NetCord.Services;
using NetCord.Services.ApplicationCommands;
using Microsoft.Extensions.Configuration;

var config = new ConfigurationBuilder()
    .AddJsonFile("appsettings.json")
    .Build();

GatewayClient client = new(new BotToken(config["Discord:Token"]), new GatewayClientConfiguration
{
    Logger = new ConsoleLogger(),
});

ApplicationCommandService<ApplicationCommandContext> applicationCommandService = new();

applicationCommandService.AddModules(typeof(Program).Assembly);

client.InteractionCreate += async interaction =>
{
    if (interaction is not ApplicationCommandInteraction applicationCommandInteraction)
        return;

    var result = await applicationCommandService.ExecuteAsync(new ApplicationCommandContext(applicationCommandInteraction, client));

    if (result is not IFailResult failResult)
        return;

    try
    {
        await interaction.SendResponseAsync(InteractionCallback.Message(failResult.Message));
    }
    catch
    {
    }
};

await applicationCommandService.RegisterCommandsAsync(client.Rest, client.Id);

await client.StartAsync();
await Task.Delay(-1);