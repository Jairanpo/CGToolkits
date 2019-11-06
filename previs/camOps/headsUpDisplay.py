from pymel.core import headsUpDisplay

headsUpDisplay('HUDFocalLength', visible=True, blockSize='small', labelFontSize='small', dataFontSize='large',
                  edit=True)
headsUpDisplay('HUDCurrentFrame', visible=True, blockSize='small', labelFontSize='small', dataFontSize='large',
                  edit=True)
headsUpDisplay('HUDCameraNames', visible=False, blockSize='small', labelFontSize='small', dataFontSize='large',
                  edit=True)
headsUpDisplay('HUDFrameRate', visible=False, edit=True)
headsUpDisplay('HUDViewAxis', visible=False, edit=True)