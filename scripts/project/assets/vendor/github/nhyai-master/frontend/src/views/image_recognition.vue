<template>
	<div id="imageRecognition">
		<Navigation></Navigation>
		<div class="top_contain">
			<el-row>
				<el-col :xs={span:24} :sm={span:11,offset:1} :md={span:10,offset:2} :lg={span:7,offset:4,pull:1} :xl={span:6,offset:5,pull:1}>
					<div class="show_title_outer">
						<h2>优图OCR</h2>
						<p class="top_describe">优图OCR基于南海云领先的深度学习算法，利用光学字符识别技术，将图片上的文字内容，
							直接转换为可编辑文本。不仅能精准快速识别身份证、名片、营业执照、驾驶证等卡证类信息，更有通用OCR和手
							写体识别技术支持更多场景、任意版面的文字信息获取，大大提高了工作效率和用户体验。</p>
					</div>
				</el-col>
				<el-col :xs={span:20,offset:2} :sm={span:11,offset:1} :md="10" :lg="8" :xl="6">
					<div >
						<img class="top_image" src="../assets/image/ocr_top_image.png" alt="">
					</div>
				</el-col>
			</el-row>
		</div>
		<div class="functional_experience">
			<h2 class="title">功能体验</h2>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<div class="show_nav">
						<ul class="clearfix">
							<li ><router-link to="/imageRecognition/idCard" >身份证OCR</router-link></li>
							<li ><router-link to="/imageRecognition/drivingLicence" >驾驶证OCR</router-link></li>
							<li ><router-link to="/imageRecognition/runningLicence" >行驶证OCR</router-link></li>
							<li ><router-link to="/imageRecognition/commonUse" >通用OCR</router-link></li>
							<li ><router-link to="/imageRecognition/businessLicence" >营业执照OCR</router-link></li>
							<li ><router-link to="/imageRecognition/bankCard" >银行卡OCR</router-link></li>
							<li ><router-link to="/imageRecognition/handwriten" >手写体OCR</router-link></li>
							<li ><router-link to="/imageRecognition/carNumber" >车牌OCR</router-link></li>
							<li ><router-link to="/imageRecognition/visitingCard" >名片OCR</router-link></li>
						</ul>
					</div>

				</el-col>
			</el-row>
			<router-view></router-view>

		</div>
		<div class="advantage_product">
			<h2 class="title">产品优势</h2>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<el-row align="left">
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image"></i>
							<div style="padding: 14px;">
								<span>通用性强</span>
								<div class="describe_outer">
									<time class="good_describe">不仅支持证照类图片，还支持多种复杂场景的文字识别，如街景门店、印刷图文等</time>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_two"></i>
							<div style="padding: 14px;">
								<span>识别精准</span>
								<div class="describe_outer">
									<time class="good_describe">单字识别准确率可达到中文98%以上，数字99%以上</time>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_three"></i>
							<div style="padding: 14px;">
								<span>适应性强</span>
								<div class="describe_outer">
									<time class="good_describe">适应各种实际应用中的异常情况，如光照不均、倾斜、模糊等，具备非常高的复杂环境可用性</time>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_four"></i>
							<div style="padding: 14px;">
								<span>服务可靠</span>
								<div class="describe_outer">
									<time class="good_describe">已成功应用于多项核心业务，历经市场验证，技术成熟稳定，可用性高达99.9%</time>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_five"></i>
							<div style="padding: 14px;">
								<span>企业级平台</span>
								<div class="describe_outer">
									<time class="good_describe">企业级图片处理大平台，保证7x24不间断云服务，让您的产品always online</time>
								</div>
							</div>
						</el-col>

					</el-row>
				</el-col>
			</el-row>
		</div>

		<div class="recommended_scenario">
			<h2 class="title">推荐场景</h2>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<el-row align="left">
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center">
							<div class="clearfix show_scenario_outer">
								<div class="fl left_image_con clearfix">
									<i class="recommended_image_one"></i>
								</div>
								<div class="fl right_word_con">
									<span>文档整理</span>
									<div class="scenario_describe_outer">
										<span class="good_describe">轻松识别图片、PDF等扫描文档中的文字，文字录入不再繁琐</span>
									</div>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center">
							<div class="clearfix show_scenario_outer">
								<div class="fl left_image_con clearfix">
									<i class="recommended_image_two"></i>
								</div>
								<div class="fl right_word_con">
									<span>物流场景</span>
									<div class="scenario_describe_outer">
										<span class="good_describe">精确识别运单上的寄件人和收件人信息，大大减轻人工输入成本</span>
									</div>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center">
							<div class="clearfix show_scenario_outer">
								<div class="fl left_image_con clearfix">
									<i class="recommended_image_three"></i>
								</div>
								<div class="fl right_word_con">
									<span>智慧医疗</span>
									<div class="scenario_describe_outer">
										<span class="good_describe">将医疗单据自动识别为文字，方便医疗信息的电子化存储和分析</span>
									</div>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center">
							<div class="clearfix show_scenario_outer">
								<div class="fl left_image_con clearfix">
									<i class="recommended_image_four"></i>
								</div>
								<div class="fl right_word_con">
									<span>身份认证</span>
									<div class="scenario_describe_outer">
										<span class="good_describe">无需手动输入证件信息，可快速进行银行身份认证、主播身份认证等</span>
									</div>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center">
							<div class="clearfix show_scenario_outer">
								<div class="fl left_image_con clearfix">
									<i class="recommended_image_five"></i>
								</div>
								<div class="fl right_word_con">
									<span>交通监管</span>
									<div class="scenario_describe_outer">
										<span class="good_describe">实时对车牌OCR，快速锁定违章车辆信息</span>
									</div>
								</div>
							</div>
						</el-col>
					</el-row>
				</el-col>
			</el-row>
		</div>
	</div>

</template>

<script>
	import Navigation from "../components/navigation.vue"
    export default {
        data() {
			return{}
        },
		components:{
            Navigation
		},

    }

</script>

<style scoped>
	.top_contain{background-color: #237EE6 ;min-height: 300px;margin-top: 80px;}
	.top_image{width: 100%;display: block;margin-top: 75px;}
	.show_title_outer{padding: 40px 20px 40px;color: white;}
	.show_title_outer h1{}
	.top_describe{font-size: 16px;margin-top: 20px;line-height: 30px;}

	.functional_experience{margin: 50px 0;}
	.functional_experience .title{text-align: center;color: #333333;margin: 40px 0;}

	.show_add_image_outer{min-height: 400px;}
	.show_top_sample{width: 100%;margin-bottom: 15px;}
	.show_nav{width: 100%;margin: 0 auto;}

	.show_nav ul{padding:15px 0;border-radius: 8px;display: flex;}
	.show_nav ul li{height:36px;border-left:1px solid #d5d5d5;border-bottom:1px solid #d5d5d5;border-top:1px solid #d5d5d5;float:left;flex: 1;overflow: hidden;}
	.show_nav ul li:last-child{border-bottom-right-radius: 5px;border-top-right-radius: 5px;border-right: 1px solid #d5d5d5;}
	.show_nav ul li:first-child{border-right:none;border-bottom-left-radius: 5px;border-top-left-radius: 5px;}
	.show_nav ul li a{height:36px;line-height:36px;font-size:16px;color:#666;display:block;text-align: center;}
	.show_nav ul li a.active{background-color:#3488ea;color:#fff;border-bottom:1px solid #3488ea;}
	.show_nav ul li a:hover{background-color:#3488ea;color:#fff;border-bottom:1px solid #3488ea;}


	.advantage_product{padding: 65px 0;overflow: hidden;background-color: #f2f2f5;}
	.advantage_product .title{text-align: center;color: #333333;margin: 50px 0;}
	.advantage_product span{display: inline-block;padding: 10px;}
	.show_word{width: 192px;height: 148px;  display: inline-block;  text-align: center;  font-size: 22px;  font-style: normal;  color: #fff;  box-sizing: border-box;  padding-top: 58px;}
	.normal_result_back{background-image: url("../assets/image/2.png"); background-position: 0 0;}
	.danger_result_back{background-image: url("../assets/image/2.png"); background-position: -196px 0;}
	.probability_number{height: 30px;line-height: 30px;text-align: center;color: #fff;font-size: 16px;margin-top: 10px;}
	.title_image{width: 80px; height: 80px;background-image: url("../assets/image/ocr/ocr_bottom_image.png");background-position: -302px -84px;display: inline-block;margin-top: 50px;}
	.title_image_two{width: 80px;  height: 80px;background-image: url("../assets/image/ocr/ocr_bottom_image.png");background-position: 0 -208px;;display: inline-block;margin-top: 50px;}
	.title_image_three{width: 80px;  height: 80px;  background-image: url("../assets/image/ocr/ocr_bottom_image.png");  background-position: -84px -208px;display: inline-block;margin-top: 50px;}
	.title_image_four{width: 80px;  height: 80px;  background-image: url("../assets/image/ocr/ocr_bottom_image.png");  background-position: -168px -208px;display: inline-block;margin-top: 50px;}
	.title_image_five{width: 80px;  height: 80px;  background-image: url("../assets/image/ocr/ocr_bottom_image.png");  background-position: -302px 0;display: inline-block;margin-top: 50px;}
	.good_describe{font-size: 14px;color: gray;}
	.describe_outer{width: 80%;margin: 0 auto;text-align: left}


	.recommended_scenario{padding: 65px 0;overflow: hidden;background-color: #fff;}
	.recommended_scenario .title{text-align: center;color: #333333;margin: 50px 0;}
	.recommended_scenario span{display: inline-block;padding: 10px;}
	.show_scenario_outer{margin-top: 15%;}
	.left_image_con{width: 30%;margin: auto 0;}
	.right_word_con{width: 70%;margin: auto 0;}
	.recommended_image_one{width: 56px;height: 56px;background-image: url("../assets/image/ocr/ocr_bottom_image.png");background-position: -149px -292px;display: inline-block;margin-top: 20px;margin-left: 35%;}
	.recommended_image_two{width: 56px;height: 56px;background-image: url("../assets/image/ocr/ocr_bottom_image.png");background-position: -209px -292px;display: inline-block;margin-top: 20px;margin-left: 35%;}
	.recommended_image_three{width: 56px;height: 56px;background-image: url("../assets/image/ocr/ocr_bottom_image.png");background-position: -89px -292px;display: inline-block;margin-top: 20px;margin-left: 35%;}
	.recommended_image_four{width: 56px;height: 56px;background-image: url("../assets/image/ocr/ocr_bottom_image.png");background-position: -302px -228px;display: inline-block;margin-top: 20px;margin-left: 35%;}
	.recommended_image_five{width: 56px;height: 56px;background-image: url("../assets/image/ocr/ocr_bottom_image.png");background-position: -302px -168px;display: inline-block;margin-top: 20px;margin-left: 35%;}
	.scenario_describe_outer{margin: 0 5px;text-align: left}
</style>