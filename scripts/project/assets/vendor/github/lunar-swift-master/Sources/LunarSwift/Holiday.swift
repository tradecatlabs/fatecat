import Foundation

@objcMembers
public class Holiday: NSObject {
    private var _day: String
    private var _name: String
    private var _work: Bool
    private var _target: String

    public var day: String {
        get {
            _day
        }
    }

    public var name: String {
        get {
            _name
        }
    }

    public var work: Bool {
        get {
            _work
        }
    }

    public var target: String {
        get {
            _target
        }
    }

    public init(day: String, name: String, work: Bool, target: String) {
        if !day.contains("-") {
            let y = day.prefix(4)
            let m = day[day.index(day.startIndex, offsetBy: 4)..<day.index(day.startIndex, offsetBy: 6)]
            let d = day.suffix(2)
            _day = "\(y)-\(m)-\(d)"
        } else {
            _day = day
        }
        _name = name
        _work = work
        if !target.contains("-") {
            let y = target.prefix(4)
            let m = target[target.index(target.startIndex, offsetBy: 4)..<target.index(target.startIndex, offsetBy: 6)]
            let d = target.suffix(2)
            _target = "\(y)-\(m)-\(d)"
        } else {
            _target = target
        }
    }

    public override var description: String {
        get {
            "\(_day) \(_name)\(_work ? "调休" : "") \(_target)"
        }
    }

}
