"use strict";
/**
 * 无限级下拉菜单
 * @author hkargc@gmail.com
 */
function infinity() {
	/**
	 * @param string elementId 要挂载SELECT的元素ID,该元素必须为空
	 * @param array data 分类数组 data[id] = [parent_id, 'cate_name'];
	 * @param int value 默认选中的值
	 */
	this.init = function(elementId, data, value, callback) {
		this.selectWidth = '100px'; //下拉表的宽度
		this.selectSize = 0; //下拉表显示的行数
		this.optionText = '--请选择--'; //下拉表默认显示
		this.optionValue = 0; //下拉表默认值
		this.element = document.getElementById(elementId); //要挂载SELECT元素的对象
		this.data = data; //分类数组,格式为: data[id] = [上级id, '显示文本'];
		this.callback = callback;
		this.element.replaceChildren(); //清空
		
		this.recursion(value); //向上递归,选中默认的值
		this.next(value); //如果还有子类
	}
	this.mkselect = function() {
		var _this = this;
		var select = document.createElement('select');
		select.size = this.selectSize;
		select.style.width = this.selectWidth;
		select.onchange = function() {
			while (this.nextSibling) {
				this.nextSibling.onchange = null; //打破循环引用?
				this.parentNode.removeChild(this.nextSibling);
			}
			_this.next(this.value);
			if(typeof(_this.callback) === 'function'){
				_this.callback();
			}
		}
		return select;
	}
	this.mkoption = function(value, text) {
		var option = document.createElement("option");
		option.setAttribute("value", value ? value : this.optionValue);
		option.appendChild(document.createTextNode(text ? text : this.optionText));
		return option;
	}
	this.recursion = function(value) {
		var select = this.mkselect(); //创建一个SELECT元素
		select.appendChild(this.mkoption()); //附加一个'请选择'下拉

		for (var i in this.data) { //如果默认为空或不存在则显示第一级
			if(this.data[i] === null){
				continue;
			}
			if(this.data[i].length <= 1){
				continue;
			}
			if (this.data[i][0] == (this.data[value] ? this.data[value][0] : 0)) {
				var option = this.mkoption(i, this.data[i][1])
				select.appendChild(option);
				option.selected = (i == value) ? 'selected' : '';
			}
		}

		if (this.element.lastChild) { //如果是上一级,则要附加在最前边,与next相反
			this.element.insertBefore(select, this.element.firstChild)
		} else {
			this.element.appendChild(select);
		}

		if (this.data[value] && this.data[value][0] != 0) { //如果上级分类不为0,向上递归
			this.recursion(this.data[value][0])
		}
	}
	this.next = function(value) {
		if (this.data[value] == undefined) {
			return false;
		}
		if (this.data[value] === null) {
			return false;
		}
		if(this.data[value].length <= 1){
			return false;
		}
		for (var i in this.data) { //查找是否有子类
			if(this.data[i] === null){
				continue;
			}
			if(this.data[i].length <= 1){
				continue;
			}
			if (this.data[i][0] == value) {
				if (typeof(select) == 'undefined') {
					var select = this.mkselect();
					select.appendChild(this.mkoption());
				}
				var option = this.mkoption(i, this.data[i][1]);
				select.appendChild(option);
				option.selected = (select.value == this.optionValue) ? 'selected' : '';
			}
		}
		if (typeof(select) != 'undefined') {
			this.element.appendChild(select);
			
			this.next(select.value); //如果还有子类
		}
	}

	this.get = function() {
		var selected = this.element.lastChild;
		var counter = 0;
		while (selected && (selected.value == this.optionValue)) { 
		
			return selected.value; //如果必须选中最末一级

			counter++;
			if(counter > 100){ //异常情况
				break;
			}
			selected = selected.previousSibling; //一直往上查直至第一个选中
		}
		if (! selected) {
			
		} else {
			return selected.value;
		}
		return this.optionValue;
	}
}