result = cmds.promptDialog(
		title='Sequence Number',
		message='Enter Sequence Number:',
		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel')
if result == 'OK':
	nSeq = cmds.promptDialog(query=True, text=True)
	print nSeq
	if nSeq == '':
		print 'Introduce a sequence number'
	else:
		digToAdd = 4 - len(nSeq)
		nSeq = str("0" * digToAdd) + str(nSeq)
		print 'kaka'
