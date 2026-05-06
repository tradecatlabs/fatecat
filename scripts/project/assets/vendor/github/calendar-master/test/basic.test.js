import * as std from '../src/basic.js';
import chai from 'chai';

let expect = chai.expect;


describe('zip operator on arrays', ()=> {
  it('zip([1,2],[3,4]) should be [[1,3],[2,4]]', ()=> {
    expect(std.zip([1,2],[3,4])).to.deep.equal([[1,3],[2,4]]);
  });
  it('zip([1,2],[3,4],[5,6]) should be [[1,3,5],[2,4,6]]', ()=> {
    expect(std.zip([1,2],[3,4],[5,6])).to.deep.equal([[1,3,5],[2,4,6]]);
  });
});

describe('zipWith operator on arrays', ()=> {
  it('zipWith((x,y)=>x+y, [1,2],[3,4]) should be [4,6]', ()=> {
    expect(std.zipWith((x,y)=>x+y,[1,2],[3,4])).to.deep.equal([4,6]);
  });
  it('zipWith((x,y,z)=>x*y+z, [1,2],[3,4],[5,6]) should be [8,14]', ()=> {
    expect(std.zipWith((x,y,z)=>x*y+z, [1,2],[3,4],[5,6])).to.deep.equal([8,14]);
  });
});

describe("omap operator for object",()=>{
  it("omap({a:3, b:4},x=>x*2) should be {a:6, b:8}", ()=>{
    expect(std.omap({a:3, b:4},x=>x*2)).to.deep.equal({a:6,b:8});
  });
});

describe("ozip operator for object",()=>{
  it("ozip({a:4,b:7},{a:6,b:1},{a:1,b:7}) should be {a:[4,6,1], b:[7,1,7]}", ()=>{
    expect(std.ozip({a:4,b:7},{a:6,b:1},{a:1,b:7})).to.deep.equal({a:[4,6,1],b:[7,1,7]});
  });
});

describe("ozipWith operator for object",()=>{
  it("ozipWith((x, y, z) => x * y + z, {a:4,b:7},{a:6,b:1},{a:1,b:7}) should be {a:25, b:14}", ()=>{
    expect(std.ozipWith((x, y, z) => x * y + z, {a:4,b:7},{a:6,b:1},{a:1,b:7})).to.deep.equal({a:25,b:14});
  });
});