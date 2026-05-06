import * as Decimal from '../../../math/decimal';
import * as Expression from '../../../math/expression';
import * as std from '../../../basic';
import * as Common from "./common";

const decimal=Decimal.decimal;
const expression=Expression.expression;
const evaluate=Expression.evaluate;


//誤差取值範圍設定為 (7.0e-7,9.0e-3) 這是兩個經驗值
const MinPrecision = decimal(7.0e-7); //該值取值範圍為 (0.6e-8, 1e-2)
const MaxPrecision = decimal(9.0e-3); //該值取值範圍為 (MinPrecision, 1e-2)

export const precision=(obj, ver, prec, t)=>{
    let p_rad=null;
    let p_au=null;
    let truncate=false;
    //誤差取值範圍 (MinPrecision,MaxPrecision)
    if (Decimal.lt(prec, MinPrecision)) prec = MinPrecision;
    if (Decimal.gt(prec, MaxPrecision)) prec = MaxPrecision;
    if (Decimal.gt(prec, Common.eps(obj, ver))) { //若prec<=p0 不截斷
        //t為距離J2000的±千年數 等於0沒意義
        if(Decimal.isZero(t))  throw new Error("Invalid span!");
            truncate=true;
            let smAxis = Common.semimajor_axis(obj, ver);
            // p(T) = prec/10/(-log(prec)-2)/(|T^α|+α|T^(α-1)|*10^-4)
            const f1=expression("prec/10/(-log(prec)-2)/(abs(T^a)+a*abs(T^(a-1))*10e-4)");
            const f2=expression("prec/10/(-log(prec)-2)");
            const P=(p, a , t)=>{
                if(a===0) return evaluate(f2,{
                    prec:p
                });
                return evaluate(f1,{
                    prec:p,
                    a:a,
                    T:t
                });
            }
            if(Decimal.lt(t,1e-15)){ //如果T充分小 則p(T)簡化為 p(T) = prec/10/(-log(prec)-2) :α=0 | ∞:α>0
                p_rad=new Array(Common.alphaMAX+1).fill(1e15); // inf= 1e15
                p_au=new Array(Common.alphaMAX+1).fill(1e15);
                p_rad[0]=P(prec,0,t);
                p_au[0]=Decimal.mult(smAxis,p_rad[0]);
            }else{
                p_rad=[...new Array(Common.alphaMAX+1).fill().keys()].map((x)=>P(prec,x,t));
                p_au=p_rad.map(x=>Decimal.mult(smAxis,x));
            }
    }
    return {
        truncate:truncate,
        p:{
            rad:p_rad,
            au:p_au
        }
    };
};
