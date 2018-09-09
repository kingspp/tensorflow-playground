var HTTPUtil = {
	GET : function(endpoint, callback) {
		$.ajax({
			type : "GET",
			url : endpoint,
			dataType : "json",
			async : false
		}).done(function(msg) {
			callback(msg, undefined);
		}).error(function(msg) {
			callback(msg, undefined);
		});
	},
	PUT : function(endpoint, callback) {
		$.ajax({
			type : "PUT",
			url : endpoint,
			dataType : "json",
			async : false
		}).done(function(msg) {
			callback(msg, undefined);
		}).error(function(msg) {
			callback(msg, undefined);
		});
	},
	POST : function(endpoint, dataBody, callback) {
		$.ajax({
			type : "POST",
			url : endpoint,
			dataType : "json",
			data : JSON.stringify(dataBody),
			contentType : "application/json; charset=utf-8"
		}).done(function(msg) {
			callback(msg, undefined);
		}).error(function(msg) {
			callback(msg, undefined);
		});

	},
	POSTFORM : function(endpoint, dataBody, callback) {
		$.ajax({
			type : "POST",
			url : endpoint,
			dataType : "json",
			data : {
				"data" : JSON.stringify(dataBody)
			},
			contentType : "application/json; charset=utf-8"
		}).success(function(msg) {
			callback(msg, undefined);
		}).error(function(msg) {
			callback(null, msg);
		});
	}
};
