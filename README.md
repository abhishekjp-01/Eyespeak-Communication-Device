# EyeSpeak Communication System (Prototype)

EyeSpeak is a **prototype assistive communication system** designed for individuals with severe physical disabilities, particularly those who are paralyzed and non-verbal.  
It enables users to communicate and control appliances using only **eye blinks**, combining **computer vision**, **embedded systems**, and **assistive technology** into a low-cost, non-invasive solution.

---

## Features
- Eye-blink detection using **Pi Camera** + **OpenCV** + **Mediapipe**  
- OLED display for real-time message output  
- Text-to-Speech conversion with speaker output  
- Control of electrical appliances (fan, light) via relay modules  
- Low-cost, portable, and non-invasive design  

---

## Hardware Components
- Raspberry Pi 4 Model B (2GB/4GB RAM)  
- Pi Camera Module  
- 0.96" OLED Display (SSD1306, I²C)  
- 2-Channel Relay Module (5V)  
- PAM8403 Audio Amplifier Module  
- 8Ω 3W Speaker  
- 5V 3A Power Supply  
- Jumper Wires  

---

## Software & Tools
- **Languages & Libraries:** Python, OpenCV, Mediapipe, luma.oled, espeak/pyttsx3  
- **IDE:** Thonny (for Raspberry Pi)  
- **Circuit Design:** Proteus  
- **OS:** Raspberry Pi OS  

---

## Working Principle
1. The Pi Camera captures real-time video of the user's face.  
2. **Eye blinks** are detected and classified as:
   - Left Blink → Scroll Up  
   - Right Blink → Scroll Down  
   - Both Eyes Blink → Select Option  
3. Selected messages are:
   - Displayed on the OLED screen  
   - Converted into speech (audio output)  
   - Used to control appliances (fan, light) via relays  



