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
    socket.write('Connected to R2D2 server.\r\n');
    socket.write('Looking for R2D2...\r\n');
    const r2d2 = await Scanner.findR2D2();
    if (r2d2) {
        socket.on('close', async function() {
            await r2d2.playAnimation(2);
            await r2d2.sleep();
            await r2d2.destroy();
        });
        socket.write('Connected to R2D2!\r\n');
        await r2d2.wake();
        await r2d2.setStance(2);
        await r2d2.playAnimation(1);
        sleep(5000)
        socket.write('Ready for commands!\r\n');
        socket.on('data', async function(buffer) {
            var command_str = buffer.toString().trim();
            console.log('Command: ' + command_str);
            var command = command_str.split(" ");
            try {
                if (command[0] == 'animate') {
                    await r2d2.playAnimation(Number(command[1]));
                    socket.write('Animation complete.\r\n');
                } else if (command[0] == 'sleep') {
                    await r2d2.sleep();
                    socket.write('Asleep.\r\n');
                } else if (command[0] == 'wake') {
                    await r2d2.wake();
                    socket.write('Awake.\r\n');
                } else if (command[0] == 'roll') {
                    var speed = Number(command[1]);
                    var angle = Number(command[2]);
                    var time = Number(command[3]);
                    await r2d2.rollTime(speed, angle, time, []);
                    socket.write('Done rolling.\r\n');
                } else if (command[0] == 'quit') {
                    await socket.destroy();
                    console.log('Socket destroyed.');
                } else if (command[0] == 'battery') {
                    var voltage = (await r2d2.batteryVoltage()).toString();
                    socket.write(voltage + '\r\n');
                } else if (command[0] == 'version') {
                    var version_map = await r2d2.appVersion();
                    var version_str = version_map.major.toString() + '.' + version_map.minor.toString();
                    socket.write(version_str + '\r\n');
                } else if (command[0] == 'set_main_led_color') {
                    var r = Number(command[1]);
                    var g = Number(command[2]);
                    var b = Number(command[3]);
                    await r2d2.setMainLedColor(r, g, b);
                    socket.write('Main LED set.\r\n');
                } else if (command[0] == 'set_back_led') {
                    var i = Number(command[1]);
                    await r2d2.setBackLedIntensity(i);
                    socket.write('Back LED set.\r\n');
                } else if (command[0] == 'set_stance') {
                    var stance_num = Number(command[1]);
                    var stance;
                    if (stance_num == 1) {
                        stance = Stance.tripod;
                    } else if (stance_num == 2) {
                        stance = Stance.bipod;
                    }
                    await r2d2.setStance(stance);
                    socket.write('Stance set.\r\n');
                } else if (command[0] == 'play_audio') {
                    var audio_num = Number(command[1]);
                    await r2d2.playAudioFile(audio_num);
                    socket.write('Audio file played.\r\n');
                } else if (command[0] == 'turn_dome') {
                    var angle = Number(command[1]);
                    await r2d2.turnDome(angle);
                    socket.write('Dome turned.\r\n');
                } else {
                    throw new Error('Illegal command.');
                }
            } catch (err) {
                console.log('Error caught: ' + err.message);
                socket.write('Illegal command.\r\n')
            }
        });
    } else {
        socket.write('Could not find R2D2.\r\n');
    }
});
server.listen(1337, '127.0.0.1');
console.log('Listening...')

/*
const WAIT_TIME: number = 1000;
const main = async () => {
  const r2d2 = await Scanner.findR2D2();
  if (r2d2) {
    await r2d2.turnDome(90);
    await Utils.wait(WAIT_TIME);
    await r2d2.turnDome(-90);
    await Utils.wait(WAIT_TIME);
    await r2d2.playAnimation(2);
    await Utils.wait(5 * WAIT_TIME);
    await r2d2.setStance(Stance.tripod);
    await Utils.wait(5 * WAIT_TIME);
    await r2d2.playAudioFile(3);
    await r2d2.setStance(Stance.bipod);
    await Utils.wait(5 * WAIT_TIME);
    await r2d2.playAnimation(5);
    await r2d2.sleep();
  }
};
main();
*/
