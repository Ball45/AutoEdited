def setup_control(self):
    self.ui.pushButton.clicked.connect(self.start_progress) 

def start_progress(self):
    max_value = 100
    self.ui.progressBar.setMaximum(max_value)

    for i in range(max_value):
        time.sleep(0.1)
        self.ui.progressBar.setValue(i+1)