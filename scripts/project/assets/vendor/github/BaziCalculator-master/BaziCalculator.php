<?php
/*
* @SandroBasta
* @BaZi Calculator
*/
class BaziCalculator
{
	public $day;
	public $month;
	
	function __construct($day,$month)
	{
		$this->day = $day;
		$this->month = $month;
	}
	public function calculateMonth(){

		switch ([$this->day,$this->month]) {
			case [$this->day <= 5 , $this->month == 1]:
				echo "Yang Earth <br /> Rat";
				break;
			case [$this->day >= 6 , $this->month == 1]:
			case [$this->day < 4 , $this->month == 2]:
				echo "Yin Earth <br /> Ox";
				break;
			case [$this->day >= 4 , $this->month == 2]:
			case [$this->day < 5 || $this->day > 31 , $this->month == 3]:
				echo "Yang Metal <br /> Tiger";
				break;
			case [$this->day >= 5, $this->month == 3]:
			case [$this->day < 4 || $this->day > 31, $this->month == 4]:
			    echo"Yin Metal <br /> Rabbit";
			    break;
			case [$this->day >= 4, $this->month == 4]:
			case [$this->day < 5 || $this->day > 31, $this->month == 5]:
			    echo"Yang Water <br /> Dragon";
			    break;
			case [$this->day >= 5, $this->month == 5]:
			case [$this->day < 5 || $this->day > 31, $this->month == 6]:
			    echo"Yin Water <br /> Snake";
			    break;
			case [$this->day >= 5, $this->month == 6]:
			case [$this->day < 7 || $this->day > 31, $this->month == 7]:
			    echo"Yang Wood <br /> Horse";
			    break;
			case [$this->day >= 7, $this->month == 7]:
			case [$this->day < 7 || $this->day > 31, $this->month == 8]:
			    echo"Yin Wood <br /> Goat";
			    break;
			case [$this->day >= 7, $this->month == 8]:
			case [$this->day < 7 || $this->day > 31, $this->month == 9]:
			    echo"Yang Fire <br /> Monkey";
			    break;
			case [$this->day >= 7, $this->month == 9]:
			case [$this->day < 8 || $this->day > 31, $this->month == 10]:
			    echo"Yin Fire <br /> Rooster";
			    break;
			case [$this->day >= 8, $this->month == 10]:
			case [$this->day < 7 || $this->day > 31, $this->month == 11]:
			    echo"Yang Earth <br /> Dog";
			    break;
			case [$this->day >= 7, $this->month == 11]:
			case [$this->day <  7 || $this->day > 31, $this->month == 12]:
			    echo"Yin Earth <br /> Pig";
			    break;
		    case [$this->day >= 7, $this->month == 12]:
			    echo"Yang Metal <br /> Rat";
			    break;
			default:
				echo "Error!";
				break;
		}
	}
	public function caclculateDay(){

	   $arrayElement = array('1'=>'Yang Wood',
	   	              '2'=>'Yin Wood',
	   	              '3'=>'Yang Fire',
	   	              '4'=>'Yin Fire',
	   	              '5'=>'Yang Earth',
	   	              '6'=>'Yin Earth',
	   	              '7'=>'Yang Metal',
	   	              '8'=>'Yin Metal',
	   	              '9'=>'Yang Water',
	   	              '0'=>'Yin Water');
	   $arrayZodiac  = array('1' => 'Rat',
	                         '2' =>  'Ox' ,
	                         '3' => 'Tiger',
	                         '4' => 'Rabbit',
	                         '5' => 'Dragon',
	                         '6' => 'Snake',
	                         '7' => 'Horse',
	                         '8' => 'Goat',
	                         '9' => 'Monkey',
	                         '10' => 'Rooster',
	                         '11' => 'Dog',
	                         '0' => 'Pig', );
	   
       $date1 = new DateTime("2016-01-01");
       $date2 = new DateTime("2016-$this->month-$this->day");
       $diff = $date2->diff($date1)->format("%a");
       $lap=$diff + 1;
       $number = 5 *(116-1) + (116-1)/4 + 15 + $lap;
       $num= floor($number);
       $element = $num%10;
       echo($arrayElement[$element]);
       echo "<br>";
       $zodiac = $num%12;
       echo($arrayZodiac[$zodiac]);

	}
}