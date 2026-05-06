#include <stdio.h>
#include "../mystl/dtoa.h"
#include "../tool.cpp"
#include <iostream>

int main(){
	Date d = {-5621,11,12,10,30,50.6987};
	// std::cout<<to_str(555)<<"\n";
	// std::cout<<to_str(555.464,2)<<"\n";
	// mystl::string ss = to_str(1234);
	// std::cout<<ss.begin() <<"\n";
	std::cout<<DD2str(d)<<"\n";
	std::cout<<"-->"<<my_stoi("12333")<<"\n";
	
	double value=-12.12345;
	char str[32];
	int len,k;
	dtoa_milo2(value, str,12, 0, &len, &k);
	
	std::cout<<value<<"\n";	
	std::cout<<len<<"!"<<k<<"\n";
}