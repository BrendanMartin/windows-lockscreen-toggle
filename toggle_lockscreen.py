import winreg
import ctypes

REG_PATH = r'SOFTWARE\Policies\Microsoft\Windows\Personalization'
SUBKEY_NAME = 'NoLockScreen'
LOCKSCREEN_ON = 0
LOCKSCREEN_OFF = 1


def toggle_lock_screen():
    try:
        winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH)
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_WRITE)
        cur_val = read_lock_value()
        new_val = 1 - cur_val
        winreg.SetValueEx(key, SUBKEY_NAME, 0, winreg.REG_DWORD, new_val)
        winreg.CloseKey(key)
        notify(read_lock_value())
    except WindowsError as e:
        print('Error: ', e)

def read_lock_value():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, REG_PATH, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, SUBKEY_NAME)
        winreg.CloseKey(key)
        return value
    except WindowsError as e:
        print('Error: ', e)

def notify(lock_status):
    msg = f"Lock screen is turned {'ON' if lock_status == LOCKSCREEN_ON else 'OFF'}"
    ctypes.windll.user32.MessageBoxW(0, msg, "Lock Screen Status", 1)


if __name__ == '__main__':
    toggle_lock_screen()