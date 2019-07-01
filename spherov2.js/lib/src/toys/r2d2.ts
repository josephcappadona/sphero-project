import { IToyAdvertisement, Stance } from './types';
import { RollableToy } from './rollable-toy';
import { IQueuePayload } from './core';

export class R2D2 extends RollableToy {
  public static advertisement: IToyAdvertisement = {
    name: 'R2-D2',
    prefix: 'D2-',
    class: R2D2
  };

  public wake(): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.power.wake());
  }
  public sleep(): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.power.sleep());
  }
  public playAudioFile(idx: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.playAudioFile(idx));
  }

  public turnDome(angle: number): Promise<IQueuePayload> {
    const res = this.calculateDomeAngle(angle);
    return this.queueCommand(this.commands.userIo.turnDome(res));
  }

  public setStance(stance: Stance): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.setStance(stance));
  }

  public playAnimation(animation: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.playAnimation(animation));
  }

  // TODO: Refractor this and simplify
  // utility calculation for dome rotation
  private calculateDomeAngle(angle: number) {
    const result = new Uint8Array(2);
    switch (angle) {
      case -1:
        result[0] = 0xbf;
        result[1] = 0x80;
        return result;
      case 0:
        result[0] = 0x00;
        result[1] = 0x00;
        return result;
      case 1:
        result[0] = 0x3f;
        result[1] = 0x80;
        return result;
    }
    let uAngle: number = Math.abs(angle);
    const hob = R2D2.hobIndex(uAngle);
    const unshift = Math.min(8 - hob, 6);
    const shift = 6 - unshift;

    // tslint:disable-next-line:no-bitwise
    uAngle = uAngle << unshift;
    if (angle < 0) {
      // tslint:disable-next-line:no-bitwise
      uAngle = 0x8000 | uAngle;
    }

    // tslint:disable-next-line:no-bitwise
    uAngle = 0x4000 | uAngle;

    // tslint:disable-next-line:no-bitwise
    const flagA = (0x04 & shift) >> 2;

    // tslint:disable-next-line:no-bitwise
    const flagB = (0x02 & shift) >> 1;

    // tslint:disable-next-line:no-bitwise
    const flagC = 0x01 & shift;
    if (flagA === 1) {
      // tslint:disable-next-line:no-bitwise
      uAngle |= 1 << 9;
    } else {
      // tslint:disable-next-line:no-bitwise
      uAngle &= uAngle ^ (1 << 9);
    }

    if (flagB === 1) {
      // tslint:disable-next-line:no-bitwise
      uAngle |= 1 << 8;
    } else {
      // tslint:disable-next-line:no-bitwise
      uAngle &= uAngle ^ (1 << 8);
    }

    if (flagC === 1) {
      // tslint:disable-next-line:no-bitwise
      uAngle |= 1 << 7;
    } else {
      // tslint:disable-next-line:no-bitwise
      uAngle &= uAngle ^ (1 << 7);
    }

    // tslint:disable-next-line:no-bitwise
    result[0] = 0x00ff & uAngle;

    // tslint:disable-next-line:no-bitwise
    result[1] = (0xff00 & uAngle) >> 8;

    return result;
  }

  private static hobIndex(val: number) {
    const values = new Uint16Array(2);
    values[1] = 0;
    values[0] = val;
    while (values[0] > 0) {
      // tslint:disable-next-line
      values[0] = values[0] >> 1;
      values[1] = values[1] + 1;
    }
    return values[1];
  }

  


  public enableCollisionDetection(): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.sensor.enableCollisionAsync());
  }

  public configureCollisionDetection(
    xThreshold: number = 100,
    yThreshold: number = 100,
    xSpeed: number = 100,
    ySpeed: number = 100,
    deadTime: number = 10,
    method: number = 0x01
  ): Promise<IQueuePayload> {
    return this.queueCommand(
      this.commands.sensor.configureCollision(
        xThreshold,
        yThreshold,
        xSpeed,
        ySpeed,
        deadTime,
        method
      )
    );
  }

  public async configureSensorStream(): Promise<IQueuePayload> {
    // 8d:0a:18:0f:0b:01:c2:d8 - response:  8d:09:18:0f:0b:00:c4:d8
    // 8d:0a:18:17:0c:00:ba:d8 - response:  8d:09:18:17:0c:00:bb:d8
    // 8d:0a:18:0c:0f:00:00:00:00:c2:d8
    // 8d:0a:18:00:4c:00:32:00:00:07:e0:78:00:d8
    // 8d:0a:18:00:0e:00:32:00:00:00:00:00:9d:d8  - payload: 00:32:00:00:00:00:00
    // await this.queueCommand(this.commands.sensor.sensor1());
    // await this.queueCommand(this.commands.sensor.sensor2());
    // await this.queueCommand(this.commands.sensor.sensorMask(
    //   [0x00, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00],
    // ));

    // I could not really figure out what this does, but according to another project, this enables certain sensors!
    // This worked to get accelorator data and pitch, yaw, roll data
    await this.queueCommand(
      this.commands.sensor.sensorMask([
        0x00,
        0x25,
        0x00,
        0x00,
        0b111,
        0b0,
        0x00
      ])
    );
    return await this.queueCommand(
      this.commands.sensor.configureSensorStream()
    );
  }


  // below taken from https://github.com/igbopie/spherov2.js/issues/31

  public setFrontAndBackLEDColor(r: number, g: number, b: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.setR2D2LEDColor(r, g, b));
  }

  public setFrontLEDColor(r: number, g: number, b: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.setR2D2FrontLEDColor(r, g, b));
  }

  public setBackLEDColor(r: number, g: number, b: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.setR2D2BackLEDcolor(r, g, b));
  }

  public setHoloIntensity(intensity: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.setR2D2HoloIntensity(intensity));
  }

  public setLogicDisplayIntensity(intensity: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.setR2D2LogicDisplayIntensity(intensity));
  }

  public setWaddle(waddleID: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.setR2D2Waddle(waddleID));
  }

  public playSound(soundID: number): Promise<IQueuePayload> {
    return this.queueCommand(this.commands.userIo.playR2D2Sound(soundID));
  }



}
