const { REST, Routes } = require('discord.js');
const { token, guildId, clientId  } = require("./config.json");

// Initialize the REST client
const rest = new REST({ version: '10' }).setToken(token);

(async () => {
    try {
        console.log('Fetching and deleting all commands...');

        // Delete global commands
        const globalCommands = await rest.get(Routes.applicationCommands(clientId));
        if (globalCommands.length > 0) {
            console.log(`Found ${globalCommands.length} global commands. Deleting...`);
            for (const command of globalCommands) {
                console.log(`Deleting global command: ${command.name} (${command.id})`);
                await rest.delete(`${Routes.applicationCommands(clientId)}/${command.id}`);
            }
        } else {
            console.log('No global commands found.');
        }

        // Delete guild commands (if guildId is provided)
        if (guildId) {
            const guildCommands = await rest.get(Routes.applicationGuildCommands(clientId, guildId));
            if (guildCommands.length > 0) {
                console.log(`Found ${guildCommands.length} guild commands. Deleting...`);
                for (const command of guildCommands) {
                    console.log(`Deleting guild command: ${command.name} (${command.id})`);
                    await rest.delete(`${Routes.applicationGuildCommands(clientId, guildId)}/${command.id}`);
                }
            } else {
                console.log('No guild commands found.');
            }
        }

        console.log('All commands deleted successfully!');
    } catch (error) {
        console.error('Error deleting commands:', error);
    }
})();
