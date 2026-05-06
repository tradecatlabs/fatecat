import * as std from '../basic.js';
import * as Decimal from './decimal';

const decimal = Decimal.decimal;

const match = (re, s) => {
    let matched = re.exec(s);
    if (matched !== null) return matched[0];
    return null;
}

const number = s => match(/^[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?/, s);
const identifier = s => match(/^[_a-zA-Z][_a-zA-Z0-9]*/, s);
const operator = s => match(/^[+\-*/%^(),]/, s);
const keywords = ["sin", "cos", "tan", "asin", "acos", "atan", "floor", "ceil", "ln", "atan2", "pow", "log"];

let lex = input => {
    input = input.replace(/\s+/g, "");
    let tokens = [],
        token;
    while (input.length > 0) {
        token = number(input);
        if (token !== null) {
            tokens.push({ type: "number", value: token });
            input = input.substr(token.length);
            continue;
        }
        token = identifier(input);
        if (token !== null) {
            tokens.push({ type: "identifier", value: token });
            input = input.substr(token.length);
            continue;
        }
        token = operator(input);
        if (token !== null) {
            tokens.push({ type: token, value: null });
            input = input.substr(token.length);
            continue;
        }
        throw new Error("Unknown token!");
    }
    tokens.push({ type: "(end)", value: null });
    return tokens;
}

let parse = tokens => {
    let symbols = {};
    const symbol = (id, nud, lbp, led) => {
        let sym = symbols[id] || {};
        symbols[id] = {
            lbp: sym.lbp || lbp,
            nud: sym.nud || nud,
            led: sym.led || led
        };
    };
    const interpretToken = token => {
        let sym = Object.create(symbols[token.type] || null);
        sym.type = token.type;
        sym.value = token.value;
        return sym;
    };
    let i = 0;
    const token = () => interpretToken(tokens[i]);
    const advance = () => { i++; return token(); };
    const expression = rbp => {
        let left, t = token();
        advance();
        if (!t.nud) throw "Unexpected token: " + t.type;
        left = t.nud(t);
        while (rbp < token().lbp) {
            t = token();
            advance();
            if (!t.led) throw "Unexpected token: " + t.type;
            left = t.led(left);
        }
        return left;
    };
    const infix = (id, lbp, rbp, led) => {
        rbp = rbp || lbp;
        symbol(id, null, lbp, led || (left => ({ type: id, left: left, right: expression(rbp) })));
    };
    const prefix = (id, rbp) => symbol(id, () => ({ type: id, right: expression(rbp) }));
    prefix("-", 7);
    infix("^", 6, 5);
    infix("*", 4);
    infix("/", 4);
    infix("%", 4);
    infix("+", 3);
    infix("-", 3);
    symbol(",");
    symbol(")");
    symbol("(end)");
    symbol("(", () => {
        let value = expression(2);
        if (token().type !== ")") throw "Expected closing parenthesis ')'";
        advance();
        return value;
    });
    symbol("number", number => number);
    symbol("identifier", name => {
        if (token().type === "(") {
            let args = [];
            if (tokens[i + 1].type === ")") advance();
            else {
                do {
                    advance();
                    args.push(expression(2));
                } while (token().type === ",");
                if (token().type !== ")") throw "Expected closing parenthesis ')'";
            }
            advance();
            return {
                type: "call",
                args: args,
                name: name.value
            };
        }
        return name;
    });
    infix("=", 1, 2, left => {
        if (left.type === "call") {
            for (var i = 0; i < left.args.length; i++) {
                if (left.args[i].type !== "identifier") throw "Invalid argument name";
            }
            return {
                type: "function",
                name: left.name,
                args: left.args,
                value: expression(2)
            };
        } else if (left.type === "identifier") {
            return {
                type: "assign",
                name: left.value,
                value: expression(2)
            };
        } else throw "Invalid lvalue";
    });
    let parseTree = [];
    while (token().type !== "(end)") {
        parseTree.push(expression(0));
    }
    return parseTree;
};
export const expression = std.memoize(s => {
    s = std.str(s);
    let tokens = lex(s);
    return parse(tokens);
});
export const evaluate = (parseTree, extern_variables, extern_functions) => {
    const operators = {
        "+": (a, b) => Decimal.plus(a, b),
        "-": (a, b) => typeof b === "undefined" ? Decimal.neg(a) : Decimal.minus(a, b),
        "*": (a, b) => Decimal.mult(a, b),
        "/": (a, b) => Decimal.div(a, b),
        "%": (a, b) => Decimal.mod(a, b),
        "^": (a, b) => Decimal.pow(a, b)
    };
    let variables = Object.assign({
        pi: Decimal.PI,
        e: Decimal.E
    }, extern_variables);
    let functions = Object.assign({
        sin: Decimal.sin,
        cos: Decimal.cos,
        tan: Decimal.tan,
        asin: Decimal.asin,
        acos: Decimal.acos,
        atan: Decimal.atan,
        abs: Decimal.abs,
        round: Decimal.round,
        ceil: Decimal.ceil,
        floor: Decimal.floor,
        log: Decimal.log,
        exp: Decimal.exp,
        sqrt: Decimal.sqrt,
        max: Decimal.max,
        min: Decimal.min,
        //random: Math.random
    }, extern_functions);
    let args = {};
    const parseNode = function(node) {
        if (node.type === "number") return decimal(node.value);
        else if (operators[node.type]) {
            if (node.left) return operators[node.type](parseNode(node.left), parseNode(node.right));
            return operators[node.type](parseNode(node.right));
        } else if (node.type === "identifier") {
            let value = args.hasOwnProperty(node.value) ? args[node.value] : variables[node.value];
            if (typeof value === "undefined") throw node.value + " is undefined";
            return value;
        } else if (node.type === "assign") {
            variables[node.name] = parseNode(node.value);
        } else if (node.type === "call") {
            let args = [];
            for (let i = 0; i < node.args.length; i++) args[i] = parseNode(node.args[i]);
            return functions[node.name].apply(null, args);
        } else if (node.type === "function") {
            functions[node.name] = function() {
                for (let i = 0; i < node.args.length; i++) {
                    args[node.args[i].value] = arguments[i];
                }
                let ret = parseNode(node.value);
                args = {};
                return ret;
            };
        }
    };
    let output = [];
    for (let i = 0; i < parseTree.length; i++) {
        let value = parseNode(parseTree[i]);
        if (typeof value !== "undefined") output.push(value);
    }
    if (output.length === 1) return output[0];
    return output;
};
