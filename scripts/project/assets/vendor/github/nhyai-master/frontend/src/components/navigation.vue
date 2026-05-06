<template>
	<div id="navigation" >
		<el-row>
			<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
				<div class="header_con clearfix">
					<a class="header_logo fl" href="http://www.hn-ssc.com">
						<!--<img :src="isNavHover?require('../assets/image/rsc_logo_white.png'):require('../assets/image/rsc_logo.png')">-->
						<img src="../assets/image/ssc_logo_white.png">
					</a>
					<ul class="header_nav fl">
						<keep-alive>
							<li><router-link to="/sindex"><span>首页</span></router-link></li>
						</keep-alive>
						<li @mouseenter="headerNavHover($event)" @mouseleave="headerNavLeave">
							<!-- <a href="javascript:;"><span class="header_point">{{$t('title.city')}}</span></a> -->
							<router-link to=""><span>图像检测</span></router-link>
							<ul class="header_nav_two">
								<li v-for="(item,index) in imageList">
									<router-link :to="item.link" @click.native="headerNavLeave">{{item.title}}</router-link>
								</li>
							</ul>
						</li>
						<li @mouseenter="headerNavHover($event)" @mouseleave="headerNavLeave">
							<!-- <a href="javascript:;"><span class="header_point">{{$t('title.city')}}</span></a> -->
							<router-link to=""><span>文本检测</span></router-link>
							<ul class="header_nav_two">
								<li v-for="(item,index) in OCRList">
									<router-link @click.native="headerNavLeave" :to="item.link">{{item.title}}</router-link>
								</li>
							</ul>
						</li>
						<!--<li><router-link to=""><span>图像检测</span></router-link></li>-->
						<!--<li><router-link to="/wordRecognition"><span>文本检测</span></router-link></li>-->
						<li><router-link to="/voiceRecognition"><span>语音识别</span></router-link></li>
						<li><router-link @click.native="headerNavLeave" to="/videoRecognition"><span>视频检测</span></router-link></li>
					</ul>
				</div>
			</el-col>
		</el-row>

	</div>

</template>

<script>
	export default {
	    name:"navigation",
		data(){
	        return{
                activeIndex: '1',
				isNavHover:false,
				imageList:[{title:"暴恐识别",link:"/force"},{title:"色情识别",link:"/yellow"}],
                OCRList:[{title:"敏感文字检测",link:"/writeRecognition"},{title:"身份证OCR",link:"/wordRecognition/idCard"},/*{title:"驾驶证OCR",link:"/wordRecognition/drivingLicence"},
					{title:"行驶证OCR",link:"/wordRecognition/runningLicence"},*/{title:"通用OCR",link:"/wordRecognition/commonUse"}/*,
                    {title:"营业执照OCR",link:"/wordRecognition/businessLicence"},{title:"银行卡OCR",link:"/wordRecognition/bankCard"},
					{title:"手写体OCR",link:"/wordRecognition/handwriten"},{title:"车牌OCR",link:"/wordRecognition/carNumber"},{title:"名片OCR",link:"/wordRecognition/visitingCard"}*/]
			}
		},
		mounted(){
            $(".header_nav_two").hide();
		},
		methods:{
            handleSelect(key, keyPath) {
                console.log(key, keyPath);
            },
            //头部导航鼠标经过事件
            headerNavHover:function(event){
                $(".header_nav_two").hide();
                $(event.currentTarget).children(".header_nav_two").show();
            },
            headerNavLeave:function(){
                $(".header_nav_two").hide();
                $(event.currentTarget).children(".header_nav_two").hide();
                console.log("离开了")
            },
		}
	}

</script>

<style>
	#navigation{height:60px;position:absolute;top:0;width: 100%;z-index: 99;background-color: transparent;min-width: 1300px;}
	#navigation :hover{background-color: #060606;}
	#navigation :hover .header_nav span{color: #fff;}
	/*#navigation :hover .header_logo img{!*display: inline-block;width: 133px;height: 58px;*!}*/
	/*#navigation :hover .header_logo img{content: url("../assets/image/nhy-logo_white.png")}*/

	/*头部样式*/
	.header_con{ min-width:800px; /*height:110px;position:absolute;top:0;left:50%;margin-left:-640px;z-index:99;*/}
	.header_logo{ margin-top:10px;}
	.header_nav{ margin-left:88px;margin-right:30px;}
	.header_nav li{height:60px;line-height:60px;display:inline-block; /* display:table-cell;vertical-align:middle; */padding: 0 20px;position:relative;}
	.header_nav li a{display:block; /* display: table-cell;vertical-align: middle; */font-size:16px; color:#fff;}
	.header_nav li a span{word-break:break-all;}
	/* .header_nav li a span.header_point{background:url(../assets/images/sindex/header_down_hover.png) no-repeat right center;padding-right:15px;} */
	/* .header_nav li a.active{height:107px;border-bottom: 3px solid #7fcd61;} */
	.header_nav li a:hover{height:60px;}
	.header_nav li a:hover span{color: #068BFF!important;}
	/* .header_nav li:hover .header_nav_two{display:block;} */
	.header_nav_two{background-color:#151414!important;box-shadow:0px 6px 8px rgba(0,0,0,0.2); position:absolute;left:0;top:60px;color:#c8c8c8;display:none;}
	.header_nav_two li{height:46px;line-height: 46px;display:block;padding:0;}
	.header_nav_two li a{ height:46px;line-height: 46px;display:block;font-size:14px;color:#fff !important;padding:0 30px;white-space:nowrap;text-align:center;}
	.header_nav_two li a:hover{height:46px;border-bottom:none;color: #fff !important;background-color:#666!important;}
	.header_nav_two li a.active{height:46px;border-bottom:none;}
	.header_link{height:80px;line-height:80px;padding-right:60px;position:relative;}
	.header_link p a{font-size:14px;color:#3488ea;}
	.header_link ul{height:36px;overflow:hidden;background:url("../assets/image/load_image_top.jpg") no-repeat 40px 17px;position:absolute;top:37px;right:0;z-index:99;cursor:pointer;border:1px solid transparent;}
	.header_link ul li{height:36px;line-height:36px;text-align:center;font-size:14px;color:#c8c8c8;padding-right:17px;padding-left:5px; }
	.header_link ul.active{height:auto;background:#fff url("../assets/image/load_image_top.jpg") no-repeat 40px 17px; border:1px solid #eee;}
	.header_link ul.active li{color:#333;}
	.header_fixed .header_nav li a{color:#fff;}
	/* .header_fixed .header_nav li a span.header_point{background:url(../assets/images/sindex/header_down_white.png) no-repeat right center;} */
	.header_fixed .header_link p a{color:#fff;}
	.header_nav li a .ru_menu_list{width:100%;height:0;line-height:50px;text-align:center;border-top:none; box-shadow: 0 13px 16px 0px rgba(0, 0, 0, 0.03);background-color:#fff; overflow:hidden; position:fixed;left:0;top:110px;z-index:99;transition:height 0.5s ease;}
	.header_nav li a .ru_menu_list a{font-size:16px; color:#333;margin:0 20px;display:inline-block;vertical-align: top;}
	.header_nav li a .ru_menu_list a:hover{color:#3488ea;height:auto;border-bottom:none;}
	.header_nav li a .ru_menu_list a.active{color:#3488ea;height:auto;border-bottom:none;}
	.ru_menu:hover .ru_menu_list{height:50px;border-top:1px solid #eaeaea;}

</style>