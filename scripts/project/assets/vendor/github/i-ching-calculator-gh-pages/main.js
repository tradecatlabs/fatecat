var outputText = "";
var opChar = true;

addEventListener("click",function(event)
{
	var text = event.path[0].textContent;

	if(opChar)
	{
		switch(text)
		{
			case "0" :
			case "1" :
			case "2" :
			case "3" :
			case "4" :
			case "5" :
			case "6" :
			case "7" :
			case "8" :
			case "9" : addOutput(text); opChar = false;
				break;
		}
	}

	else
	{
		switch(text)
		{
			case "/" : opChar = true;
			case "*" : opChar = true;
			case "+" : opChar = true;
			case "-" : opChar = true;
			case "0" :
			case "1" :
			case "2" :
			case "3" :
			case "4" :
			case "5" :
			case "6" :
			case "7" :
			case "8" :
			case "9" : addOutput(text);
				break;
			}
	}

	switch(text)
	{
		case "delete" : deleteChar(); opChar = false;
			break;
		case "clear all" : clearAll(); opChar = true;
			break;
		case "equals" : calaculate(); opChar = false;
			break;
	}
});

function calaculate()
{
	var result;
	var nums = [];
	var oper = [];
	var temp = "";

	for(var i in outputText)
	{
		var c = outputText[i];

		if(c == "/" || c == "*" || c == "-" || c == "+")
		{
			nums.push(Number(temp));
			temp = "";
			oper.push(c);
		}

		else temp += c;

		if(i == outputText.length - 1)
		{
			nums.push(Number(temp));
			temp = "";
		}
	}

	result = nums[0];

	for(var j = 1;j<nums.length;j++)
	{
		if(oper[j-1] == "+")
		{
			result += nums[j];
		}

		else if(oper[j-1] == "-")
		{
			result -= nums[j];
		}

		else if(oper[j-1] == "*")
		{
			result *= nums[j];
		}

		else if(oper[j-1] == "/")
		{
			result /= nums[j];
		}
	}

	if(result > 4)
	{
		outputText = "suffusion of yellow";
		updateOutput();
		outputText = "";
	}

	else
	{
		outputText = String(result);
		updateOutput();
	}
}

function clearAll()
{
	outputText = "";
	updateOutput();
}

function deleteChar()
{
	var i = outputText.length - 1;

	outputText = outputText.slice(0, i);

	updateOutput();
}

function addOutput(text)
{
	outputText += text;
	updateOutput();
}

function updateOutput()
{
	document.getElementById("output").textContent = outputText;
}
