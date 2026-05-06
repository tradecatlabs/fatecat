import Foundation

@objcMembers
public class FotoFestival: NSObject {
    private var _name: String
    private var _result: String
    private var _everyMonth: Bool
    private var _remark: String

    public var name: String {
        get {
            _name
        }
    }

    public var result: String {
        get {
            _result
        }
    }

    public var everyMonth: Bool {
        get {
            _everyMonth
        }
    }

    public var remark: String {
        get {
            _remark
        }
    }

    public init(name: String, result: String = "", everyMonth: Bool, remark: String = "") {
        _name = name
        _result = result
        _everyMonth = everyMonth
        _remark = remark
    }

    public override var description: String {
        get {
            "\(_name)"
        }
    }

    public var fullString: String {
        get {
            var s = "\(_name)"
            if _result.count > 0 {
                s.append(" \(_result)")
            }
            if _remark.count > 0 {
                s.append(" \(_remark)")
            }
            return s
        }
    }

}
