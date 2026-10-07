using NetCord.Rest;
using NetCord.Services.ApplicationCommands;
using Comet.Utils;

namespace Comet.Commands;

public abstract class BaseCommand : ApplicationCommandModule<ApplicationCommandContext>
{
    protected Task Respond(EmbedProperties embed)
    {
        return Context.Interaction.SendResponseAsync(
            InteractionCallback.Message(
                new InteractionMessageProperties
                {
                    Embeds = [embed]
                }
            )
        );
    }

    protected Task Respond(string message)
    {
        return Context.Interaction.SendResponseAsync(
            InteractionCallback.Message(
                new InteractionMessageProperties
                {
                    Content = message
                }
            )
        );
    }

    protected Task RespondError(string message)
    {
        EmbedProperties embed = new()
        {
            Title = message,
            Color = Colors.Error
        };

        return Context.Interaction.SendResponseAsync(
            InteractionCallback.Message(
                new InteractionMessageProperties
                {
                    Embeds = [embed]
                }
            )
        );
    }
}
