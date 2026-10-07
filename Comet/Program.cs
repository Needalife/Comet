using Comet.Services.FFXIV;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using NetCord.Hosting.Gateway;
using NetCord.Hosting.Services;
using NetCord.Hosting.Services.ApplicationCommands;

var builder = Host.CreateApplicationBuilder(args);

builder.Services
    .AddDiscordGateway(options => { 
        options.Token = builder.Configuration["Discord:Token"]!; 
    })
    .AddApplicationCommands();

builder.Services.AddHttpClient<Universalis>();

var host = builder.Build();

host.AddModules(typeof(Program).Assembly);

await host.RunAsync();