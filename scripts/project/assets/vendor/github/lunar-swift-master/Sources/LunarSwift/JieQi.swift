import Foundation

@objcMembers
public class JieQi: NSObject {
    private var _name: String
    private var _solar: Solar
    private var _jie: Bool = false
    private var _qi: Bool = false

    public var name: String {
        get {
            _name
        }
    }

    public var jie: Bool {
        get {
            _jie
        }
    }

    public var qi: Bool {
        get {
            _qi
        }
    }

    public var solar: Solar {
        get {
            _solar
        }
    }

    public init(name: String, solar: Solar) {
        _name = name
        _solar = solar
        for i in (0..<Lunar.JIE_QI.count) {
            if name != Lunar.JIE_QI[i] {
                continue
            }
            if i % 2 == 0 {
                _qi = true
            } else {
                _jie = true
            }
            return
        }
    }

    public override var description: String {
        "\(_name)"
    }

}
