# auto-trader (WIP)
This project is an auto trader script for Pokémon GO, using [scrcpy](https://github.com/Genymobile/scrcpy) to both capture the phone's screen and controling it.

⚠️ Take a look at their FAQ before asking here

## How to use

1. Open *user1*'s app on fullscreen
1. Open *user2*'s on floating-window mode, and fix it to **top left** of the screen with **default size**
1. Open `scrcpy` now (if it is not already)
1. Run `auto-trader`
   - Input *user2*'s nickname
   - Input both tag names
   - Click start button

## Warnings
- My main idea is to make the trading loop as robust to errors as possible, however keep in mind that it is not 100% tested and migth fail, so you shall supervise it, at least the first times
- It will fail if you move or change the size of `scrcpy`'s window, so don't do that after the start button is pressed
- The scripts needs some constants:
  - PC screen size
  - Position of some buttons on `scrcpy`'s window
They migth need to be adjusted depending on your monitor/phone, they are easily find at the top of the file
- Code designed for Windows (API used to simulate input)
- As the script takes control of the mouse (and keyboard for a brief moment at the start), you won't be able to use your mouse during the trades, but you could for example watch a movie
