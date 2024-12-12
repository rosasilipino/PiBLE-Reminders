# PiBLE-Reminders
## CS578 Wireless Networks Final Project.

### Group 15: Rosa Silipino, Jose Urrutia, Alberto Escalante

#### Reminder System based on BLE proximity to Pi3B+ acting as the beacon. Reminders stored on reminders.json file.
#### Device is tracked by associated MAC's BLE broadcasts, if device passes threshold reminders are sent via IFTT.

##### Hardware: 
- Raspberry Pi Model 3 B+
- ROADOM 7’’ Touch Screen

##### Software:
- **Python** for scripts.
- **HTML** and **CSS** for front-end REST API
- **If This The That (IFTTT)** for Notification services.
- **Bleak** for BLE monitoring in *ble.py*
- **Flask** for REST API creation
