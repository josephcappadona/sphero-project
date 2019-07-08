import { Scanner, Stance, Utils } from 'spherov2.js';
import { R2D2, R2Q5 } from 'spherov2.js';
import { sounds_array } from 'spherov2.js';
const net = require('net');
const fs = require('fs');

function sleep(milliseconds) {
    var start = new Date().getTime();
    while (true) {
        if ((new Date().getTime() - start) > milliseconds){
            break;
        }
    }
}

var server = net.createServer(async function(socket) {

    var socketID = `${socket.remoteAddress}:${socket.remotePort}`;

    socket.write('Connected to Sphero server.\r\n');
    console.log(`Connected to client (${socketID}).`)
    var droid;

    socket.on('close', async function() {
        if (droid !== undefined) {
            try { await droid.destroy(); }
            catch { console.log('Exception caught while destroying droid.'); };
        }
        try { await socket.destroy(); }
            catch { console.log('Exception caught while destroying socket.'); };
    });

    socket.on('data', async function(buffer) {

        var command_str = buffer.toString().trim();
        console.log(`${socketID}: ${command_str}`);

        var command = command_str.split(" ");

        if (command[0] == 'help') {
            //fetch('/help_text.txt').then(response => response.text()).then(text => socket.write(`${text}\r\n`))
            fs.readFile(`${__dirname}/help_text.txt`, (err, data) => {
                if (err) throw err;

                socket.write(`${data.toString()}\r\n`);
            })
            return
        }

        try {
            if (droid === undefined || command[0] == 'scan') {
                if (command[0] == 'connect') {
                    if (command.length > 1) {
                        if (command[1] == 'R2D2') {
                            droid = await Scanner.findR2D2();
                            if (droid === undefined) {
                                socket.write('Could not connect to any R2D2. Make sure it is charged and in range.\r\n');
                                console.log('Could not connect to any R2D2.');
                            } else {
                                const droidName = droid.peripheral.advertisement.localName;
                                socket.write(`Connected to ${droidName}!\r\n`);
                                console.log(`Connected to ${droidName}.`);
                                droid.wake();
                                droid.setStance(2);
                                droid.playAnimation(2);
                                sleep(3000);
                                socket.write('Ready for commands!\r\n');
                            }
                        } else if (command[1] == 'R2Q5') {
                            droid = await Scanner.findR2Q5();
                            if (droid === undefined) {
                                socket.write('Could not connect to any R2Q5. Make sure it is charged and in range.\r\n');
                                console.log('Could not connect to any R2Q5.');
                            } else {
                                const droidName = droid.peripheral.advertisement.localName;
                                socket.write(`Connected to ${droidName}!\r\n`);
                                console.log(`Connected to ${droidName}.`);
                                droid.wake();
                                droid.setStance(2);
                                droid.playAnimation(2);
                                sleep(3000);
                                socket.write('Ready for commands!\r\n');
                            }
                        } else {
                            const droidName = command[1];
                            const droidIdentifier = command[1].substring(0,2);
                            if (droidIdentifier == 'D2') {
                                droid = await Scanner.findR2D2ByName(droidName);
                            } else if (droidIdentifier == 'Q5') {
                                droid = await Scanner.findR2Q5ByName(droidName);
                            } else {
                                throw new Error(`Illegal prefix ${droidIdentifier}`);
                            }
                            if (droid !== undefined) {
                                socket.write(`Connected to ${droidName}!\r\n`);
                                console.log(`Connected to ${droidName}.`);
                                droid.wake();
                                droid.setStance(2);
                                droid.playAnimation(2);
                                sleep(3000);
                                socket.write('Ready for commands!\r\n');
                            } else {
                                socket.write(`Could not connect to ${droidName}. Make sure it is charged and in range.\r\n`);
                                console.log(`Could not to connect to ${droidName}.`);
                            }
                        }
                    } else {
                        droid = await Scanner.findR2D2();
                        if (droid === undefined) {
                            droid = await Scanner.findR2Q5();
                            if (droid === undefined) {
                                socket.write('Could not connect to any droids. Make sure they are charged and in range.\r\n');
                            } else {
                                const droidName = droid.peripheral.advertisement.localName;
                                socket.write(`Connected to ${droidName}!\r\n`);
                                console.log(`Connected to ${droidName}.`);
                                droid.wake();
                                droid.setStance(2);
                                droid.playAnimation(2);
                                sleep(3000);
                                socket.write('Ready for commands!\r\n');
                            }
                        } else {
                            const droidName = droid.peripheral.advertisement.localName;
                            socket.write(`Connected to ${droidName}!\r\n`);
                            console.log(`Connected to ${droidName}.`);
                            droid.wake();
                            droid.setStance(2);
                            droid.playAnimation(2);
                            sleep(3000);
                            socket.write('Ready for commands!\r\n');
                        }
                    }
                } else if (command[0] == 'scan') {
                    socket.write('Scanning for droids...\r\n');
                    var foundToys = await Scanner.findToys([R2D2.advertisement, R2Q5.advertisement]);
                    socket.write(`Done scanning. ${foundToys.length} droid${(foundToys.length == 1)? '' : 's'} found.\n`);

                    const R2D2sFound = foundToys.filter(toy => toy.prefix == R2D2.advertisement.prefix);
                    if (R2D2sFound.length > 0) {
                        socket.write('\nR2D2s:\n');
                        R2D2sFound.forEach(function(toy) {
                            socket.write(`\t${toy.peripheral.advertisement.localName}\n`);
                            socket.write(`\t\taddress: ${toy.peripheral.address}\n`);
                            socket.write(`\t\tuuid: ${toy.peripheral.uuid}\n`);
                            socket.write(`\t\trssi: ${toy.peripheral.rssi}\n`);
                        });
                    }

                    const R2Q5sFound = foundToys.filter(toy => toy.prefix == R2Q5.advertisement.prefix);
                    if (R2Q5sFound.length > 0) {
                        socket.write('\nR2Q5s:\n');
                        R2Q5sFound.forEach(function(toy) {
                            socket.write(`\t${toy.peripheral.advertisement.localName}\n`);
                            socket.write(`\t\taddress: ${toy.peripheral.address}\n`);
                            socket.write(`\t\tuuid: ${toy.peripheral.uuid}\n`);
                            socket.write(`\t\trssi: ${toy.peripheral.rssi}\n`);
                        });
                    }
                    socket.write('\r\n')

                } else if (command[0] == 'quit' || command[0] == 'exit') {
                    await socket.destroy();
                    console.log(`Socket (${socketID}) destroyed.`);
                }
            } else {
                const droidName = droid.peripheral.advertisement.localName;

                if (command[0] == 'animate') {
                    await droid.playAnimation(Number(command[1]));
                    socket.write('Animation complete.\r\n');

                } else if (command[0] == 'sleep') {
                    await droid.sleep();
                    socket.write('Asleep.\r\n');

                } else if (command[0] == 'wake') {
                    await droid.wake();
                    socket.write('Awake.\r\n');

                } else if (command[0] == 'turn') {
                    var angle = Number(command[1]);

                    await droid.rollTime(0, angle, 0.5, []);
                    socket.write('Done turning.\r\n')
                } else if (command[0] == 'roll_time') {
                    var speed = 255*Number(command[1]);
                    var angle = Number(command[2]);
                    var time = 1000*Number(command[3]);

                    await droid.rollTime(speed, angle, time, []);
                    socket.write('Done rolling.\r\n');

                } else if (command[0] == 'roll_continuous') {
                    var speed = 255*Number(command[1]);
                    var angle = Number(command[2]);

                    socket.write('Initializing rolling.\r\n');
                    await droid.roll(speed, angle, []);

                } else if (command[0] == 'quit' || command[0] == 'exit') {
                    await droid.sleep();
                    await droid.destroy();
                    await socket.destroy();
                    console.log(`Socket (${socketID}) destroyed.`);
                    droid = undefined;

                } else if (command[0] == 'disconnect') {
                    await droid.sleep();
                    await droid.destroy();
                    console.log(`Disconnected ${socketID} from ${droidName}.`);
                    socket.write(`Disconnected from ${droidName}.\r\n`);
                    droid = undefined;

                } else if (command[0] == 'battery') {
                    var voltage = (await droid.batteryVoltage()).toString();
                    socket.write(voltage + '\r\n');

                } else if (command[0] == 'version') {
                    var version_map = await droid.appVersion();
                    var version_str = version_map.major.toString() + '.' + version_map.minor.toString();
                    socket.write(version_str + '\r\n');

                } else if (command[0] == 'set_front_led_color') {
                    var r = Number(command[1]);
                    var g = Number(command[2]);
                    var b = Number(command[3]);

                    await droid.setFrontLEDColor(r, g, b);
                    socket.write('Front LED set.\r\n');

                } else if (command[0] == 'set_back_led_color') {
                    var r = Number(command[1]);
                    var g = Number(command[2]);
                    var b = Number(command[3]);

                    await droid.setBackLEDColor(r, g, b);
                    socket.write('Back LED set.\r\n');

                } else if (command[0] == 'set_stance') {
                    var stance_num = Number(command[1]);
                    var stance = 0;
                    if (stance_num == 1) {
                        stance = Stance.tripod;
                    } else if (stance_num == 2) {
                        stance = Stance.bipod;
                    }

                    await droid.setStance(stance);
                    socket.write('Stance set.\r\n');

                } else if (command[0] == 'play_sound') {
                    var audio_num = Number(command[1]);
                    await droid.playSound(audio_num);
                    socket.write(`Sound (${sounds_array[audio_num].soundId}) played.\r\n`);

                } else if (command[0] == 'turn_dome') {
                    var angle = Number(command[1]);
                    await droid.turnDome(angle);
                    socket.write('Dome turned.\r\n');

                } else if (command[0] == 'set_waddle') {
                    var waddleID = (Number(command[1]) == 1) ? 3 : 0;
                    
                    await droid.setWaddle(waddleID);
                    socket.write('Waddle set.\r\n');

                } else if (command[0] == 'set_holo_intensity') {
                    var intensity = 255*Number(command[1]);
                    await droid.setHoloIntensity(intensity);
                    socket.write('Holo projector intensity set.\r\n');

                } else if (command[0] == 'set_logic_intensity') {
                    var intensity = 255*Number(command[1]);
                    await droid.setLogicDisplayIntensity(intensity);
                    socket.write('Logic display intensity set.\r\n');

                } else {
                    throw new Error('Illegal command.');
                }
            }
        } catch (err) {
            console.log(`Error caught: ${err.message}`);
            socket.write(`${err.message}\r\n`);
        }
    });
});
server.listen(1337, '127.0.0.1');
console.log('Listening...')
