import { Scanner, Stance, Utils } from 'spherov2.js';

const WAIT_TIME: number = 1000;

const main = async () => {
  const r2d2 = await Scanner.findR2D2();
  if (r2d2) {
    await r2d2.wake();

    await r2d2.turnDome(-90);
    await Utils.wait(WAIT_TIME);

    await r2d2.turnDome(90);
    await Utils.wait(WAIT_TIME);

    await r2d2.setFrontLEDColor(255, 0, 0);
    await r2d2.setBackLEDColor(0, 255, 0);
    await r2d2.setHoloIntensity(255);
    await r2d2.setLogicDisplayIntensity(255);
    await Utils.wait(WAIT_TIME);


    await r2d2.playAnimation(2);
    await Utils.wait(5 * WAIT_TIME);
    
    await r2d2.setWaddle(3);
    await Utils.wait(5 * WAIT_TIME);

    await r2d2.setWaddle(0);
    await r2d2.setStance(Stance.bipod);
    await Utils.wait(WAIT_TIME);

    await r2d2.setStance(Stance.tripod);
    await Utils.wait(3 * WAIT_TIME);
    
    await r2d2.playSound(3);
    await Utils.wait(3 * WAIT_TIME);
    
    await r2d2.sleep();
    await r2d2.destroy();
  }
};

main();
