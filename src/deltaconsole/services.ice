module DeltaIce
{
	class DObject
	{
	};
	
	class DateTimePure
	{
		short year;
		byte month;
		byte day;
		byte hour;
		byte minute;
		byte second;
		int microsecond;
	};
	
	exception GenericException
	{
		string code;
		string message;
		string traceback;
		DObject data;
	};
	
	exception AuthenticationException extends GenericException
	{
	};

	sequence<byte> DBuffer;
	sequence<DObject> DList;
	dictionary<string, DObject> DDictionary;
	
	class IntObject extends DObject
	{
		int value;
	};
	
	class LongObject extends DObject
	{
		long value;
	};
	
	class DoubleObject extends DObject
	{
		double value;
	};
	
	class StringObject extends DObject
	{
		string value;
	};
	
	class BoolObject extends DObject
	{
		bool value;
	};
	
	class DecimalObject extends DObject
	{
		string value;
	};
	
	class DateTimeObject extends DObject
	{
		DateTimePure value;
	};
	
	class BufferObject extends DObject
	{
		DBuffer value;
	};
	
	class DictObject extends DObject
	{
		DDictionary value;
	};
	
	class ListObject extends DObject
	{
		DList value;
	};
	
	interface IIceDispatcher
	{
		StringObject login(StringObject userName, StringObject password, DDictionary options) throws GenericException, AuthenticationException;
		DObject execute(StringObject ticket, StringObject userName, StringObject commandKey, DList args, DDictionary kwargs) throws GenericException;
		void logout(StringObject ticket, StringObject userName) throws GenericException;
	};
};
