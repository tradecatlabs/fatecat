import Foundation

@objcMembers
public class TaoFestival: NSObject {
    private var _name: String
    private var _remark: String

    public var name: String {
        get {
            _name
        }
    }

    public var remark: String {
        get {
            _remark
        }
    }

    public init(name: String, remark: String = "") {
        _name = name
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
            if _remark.count > 0 {
                s.append(_remark)
            }
            return s
        }
    }

}
