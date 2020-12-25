#!/usr/bin/env python

import win

app = win.window()
app.root.protocol("WM_DELETE_WINDOW", app.main_closing)
app.root.mainloop()