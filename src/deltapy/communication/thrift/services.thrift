exception GenericException {
	1: string code,
	2: string message,
	3: string traceback,
	4: DObject data
}

exception AuthenticationException {
	1: string code,
	2: string message,
	3: string traceback,
	4: DObject data,
	5: optional string user
}

exception JsonGenericException {
	1: string code,
	2: string message,
	3: string traceback,
	4: string data
}

exception JsonAuthenticationException {
	1: string code,
	2: string message,
	3: string traceback,
	4: string data,
	5: optional string user
}

struct DateTimePure {
	1: i32 year,
	2: byte month,
	3: byte day,
	4: byte hour,
	5: byte minute,
	6: byte second,
	7: i32 microsecond
}

typedef list<byte> DBuffer

struct DObject {
	1: optional i32 integerValue,
	2: optional i64 longValue,
	3: optional double doubleValue,
	4: optional string stringVvalue,
	5: optional bool boolValue,
	6: optional DateTimePure dateTimeValue,
	7: optional DBuffer bufferValue
}

struct DictObject {
	1: optional DObject value,
	2: optional map<string, DictObject> children
}

struct ListObject {
	1: optional DObject value,
	2: optional list<ListObject> children
}

service DeltaThriftDispatcher {
	string login(1:string userName, 2:string password, 3:DictObject options) throws (1:GenericException genericException, 2:AuthenticationException authenticationException),
	DictObject loginEx(1:string userName, 2:string password, 3:DictObject options) throws (1:GenericException genericException, 2: AuthenticationException authenticationException),
	DictObject execute(1:string ticket, 2:string userName, 3:string commandKey, 4:ListObject arguments, 5:DictObject keywordArguments) throws (1:GenericException genericException),
	DictObject executeEx(1:DictObject request) throws (1:GenericException genericException),
	void logout(1:string ticket, 2:string userName) throws (1:GenericException genericException)
}