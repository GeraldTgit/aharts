from backend.public_backend import *
from backend.logs_generator import log_message

@lru_cache(maxsize=None)
def return_to_previous_page(self, main_window):
    # Show the main form and hide the current open form
    try:
        main_window.show()
        self.close()  # Close the current form
    except Exception as e:
        message = f"Error returning to main form: {e}"
        log_message(message)
        QMessageBox.information(None, "AHARTS", message) 
        sys.exit()
