import { Scanner, Stance, Utils } from 'spherov2.js';
var net = require('net');

function sleep(milliseconds) {
	var start = new Date().getTime();
    while (true) {
		if ((new Date().getTime() - start) > milliseconds){
			break;
		}
	}
}

var server = net.createServer(async function(socket) {

    socket.write('Connected to R2Q5 server.\r\n');
    socket.write('Looking for R2Q5...\r\n');
    const r2q5 = await Scanner.findR2Q5();

    if (r2q5) {

        socket.on('close', async function() {
            try { await r2q5.destroy(); }
                catch { console.log('Exception caught while destroying r2q5.'); };
            try { await socket.destroy(); }
                catch { console.log('Exception caught while destroying socket.'); };
        });

        socket.write('Connected to R2Q5!\r\n');
        await r2q5.wake();
        await r2q5.setStance(2);
        await r2q5.playAnimation(2);
        sleep(3000)
        socket.write('Ready for commands!\r\n');

        socket.on('data', async function(buffer) {

            var command_str = buffer.toString().trim();
            console.log('Command: ' + command_str);

            var command = command_str.split(" ");
            try {
                if (command[0] == 'animate') {
                    await r2q5.playAnimation(Number(command[1]));
                    socket.write('Animation complete.\r\n');

                } else if (command[0] == 'sleep') {
                    await r2q5.sleep();
                    socket.write('Asleep.\r\n');

                } else if (command[0] == 'wake') {
                    await r2q5.wake();
                    socket.write('Awake.\r\n');

                } else if (command[0] == 'roll') {
                    var speed = Number(command[1]);
                    var angle = Number(command[2]);
                    var time = Number(command[3]);

                    await r2q5.rollTime(speed, angle, time, []);
                    socket.write('Done rolling.\r\n');

                } else if (command[0] == 'quit') {
                    await r2q5.sleep();
                    await r2q5.destroy();
                    await socket.destroy();
                    console.log('Socket destroyed.');

                } else if (command[0] == 'battery') {
                    var voltage = (await r2q5.batteryVoltage()).toString();
                    socket.write(voltage + '\r\n');

                } else if (command[0] == 'version') {
                    var version_map = await r2q5.appVersion();
                    var version_str = version_map.major.toString() + '.' + version_map.minor.toString();
                    socket.write(version_str + '\r\n');

                } else if (command[0] == 'set_main_led_color') {
                    var r = Number(command[1]);
                    var g = Number(command[2]);
                    var b = Number(command[3]);

                    await r2q5.setMainLedColor(r, g, b);
                    socket.write('Main LED set.\r\n');

                } else if (command[0] == 'set_back_led') {
                    var i = Number(command[1]);
                    await r2q5.setBackLedIntensity(i);
                    socket.write('Back LED set.\r\n');

                } else if (command[0] == 'set_stance') {
                    var stance_num = Number(command[1]);
                    var stance = 0;
                    if (stance_num == 1) {
                        stance = Stance.tripod;
                    } else if (stance_num == 2) {
                        stance = Stance.bipod;
                    }

                    await r2q5.setStance(stance);
                    socket.write('Stance set.\r\n');

                } else if (command[0] == 'play_audio') {
                    var audio_num = Number(command[1]);
                    await r2q5.playAudioFile(audio_num);
                    socket.write('Audio file played.\r\n');

                } else if (command[0] == 'turn_dome') {
                    var angle = Number(command[1]);
                    await r2q5.turnDome(angle);
                    socket.write('Dome turned.\r\n');

                } else {
                    throw new Error('Illegal command.');
                }

            } catch (err) {
                console.log('Error caught: ' + err.message);
                socket.write('Illegal command.\r\n');
            }
        });
    } else {
        socket.write('Could not find R2Q5.\r\n');
    }
});
server.listen(1338, '127.0.0.1');
console.log('Listening...')
