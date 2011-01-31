this.Forms =
	_id: "_design/forms"
	views:
		pending:
			map: (doc) -> 
				emit(doc.filename, null) if doc.status == "pending"
		filename:
			map: (doc) ->
				emit(doc.filename, doc)