<template>
	<div id="wordRecognition">
		<Navigation></Navigation>
		<div class="word_top_contain">
			<el-row>
				<el-row>
					<el-col :xl={span:24}>
						<div class="banner_outer ai-common-banner">
							<!--<img src="../assets/image/word/word_banner.png" alt="">-->
							<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
								<div class="describe_outer_banner">
									<p class="ell">卡证类识别</p>
									<p class="ell-rows-4 ">基于南海云网络领先的深度学习算法，利用光学字符识别技术，将图片上的文字内容，直接转换为可编辑文本。不仅能精准快速识别身份证、名片、营业执照、驾驶证等卡证类信息，更有通用OCR和手写体识别技术支持更多场景、任意版面的文字信息获取，大大提高了工作效率和用户体验。</p>
									<p class="practice_online" @click="toPractice">在线体验</p>
								</div>
							</el-col>
						</div>
					</el-col>
				</el-row>
			</el-row>
		</div>
		<div class="functional_introduce">
			<p class="title">功能介绍</p>
			<div class="handwrite">
				<el-row>
					<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
						<!--<p class="title_describe">智能识别含有宣扬恐怖主义、极端主义、血腥、政治游行等画面的暴恐及反动内容。暴恐识别模型更为严格，对涉嫌暴恐信息零容忍，为您的产品保驾护航，远离涉暴涉恐风险。</p>-->
						<div class="word_introduce_outer">
							<ul class="clearfix" >
								<li class=" fl" v-for="item in introduceList">
									<div class="describe_image_outer">
										<img :src="item.src" alt="">
									</div>

									<div class="introduce_describe_outer ell-rows-3">
										<p>{{item.title}}</p>
										<span>{{item.des}}</span>
									</div>
								</li>
							</ul>
						</div>
					</el-col>
				</el-row>
			</div>
		</div>
		<div class="functional_experience" id="practice_title">
			<p class="title">功能体验</p>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<div class="show_nav">
						<ul class="clearfix">
							<li ><router-link to="/wordRecognition/idCard" >身份证识别</router-link></li>
							<li ><router-link to="/wordRecognition/commonUse" >通用识别</router-link></li>
							<!--<li ><router-link to="/wordRecognition/runningLicence" >行驶证识别</router-link></li>
							<li ><router-link to="/wordRecognition/drivingLicence" >驾驶证识别</router-link></li>
							<li ><router-link to="/wordRecognition/businessLicence" >营业执照识别</router-link></li>
							<li ><router-link to="/wordRecognition/bankCard" >银行卡识别</router-link></li>
							<li ><router-link to="/wordRecognition/handwriten" >手写体识别</router-link></li>
							<li ><router-link to="/wordRecognition/carNumber" >车牌识别</router-link></li>
							<li ><router-link to="/wordRecognition/visitingCard" >名片识别</router-link></li>-->
						</ul>
					</div>
				</el-col>
			</el-row>
			<router-view></router-view>
		</div>
		<div class="recommended_scenario">
			<p class="title">应用场景</p>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:16,offset:4} :xl={span:14,offset:5}>
					<ul>
						<li>
							<p>远程身份认证</p>
							<span>结合OCR和人脸识别技术，实现用户证件信息的自动录入，并完成用户身份验证。应用于金融保险、社保O2O等行业，有效控制业务风险</span>
						</li>
						<li>
							<p>内容审核与监管</p>
							<span>自动识别图片、视频中的文字内容，及时发现涉黄、涉暴、政治敏感、恶意广告等不合规内容，规避业务风险，大幅节约人工审核成本</span>
						</li>
						<li>
							<p>纸质文档票据电子化</p>
							<span>通过OCR实现纸质文档资料、票据、表格的自动识别和录入，减少人工录入成本，提高输入效率 </span>
						</li>
					</ul>
				</el-col>
			</el-row>
		</div>
		<div class="advantage_product">
			<h2 class="title">技术优势</h2>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<el-row align="left">
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image title_image_common"></i>
							<div class="show_advantage_describe">
								<span>准确率高</span>
								<div class="describe_outer">
									<p class="good_describe">目前准确率可达90%以上，基于智能的深度学习算法，准确度还将不断提高。</p>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_two title_image_common"></i>
							<div class="show_advantage_describe">
								<span>及时高效</span>
								<div class="describe_outer">
									<p class="good_describe">不仅支持证照类图片，还支持多种复杂场景的文字识别，如街景门店、印刷图文等</p>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_three title_image_common"></i>
							<div class="show_advantage_describe">
								<span>灵活性定制</span>
								<div class="describe_outer">
									<p class="good_describe">适应各种实际应用中的异常情况，如光照不均、倾斜、模糊等，具备非常高的复杂环境可用性</p>
								</div>
							</div>
						</el-col>
					</el-row>
				</el-col>
			</el-row>
		</div>
		<FooterIndex></FooterIndex>
	</div>

</template>

<script>
    import {scrollBy} from '../store/common'
	import Navigation from "../components/navigation.vue"
    import FooterIndex from "../components/footerIndex.vue"
    export default {
        data() {
			return{
                dialogImageUrl: "",
                dialogVisible: false,
                jsonDemo:'{"ret":0,"msg":"ok","data":{"tag_list":[{"tag_name":"protest","probability":0.3087675468623638},{"tag_name":"violence","probability":0.017580988407135},{"tag_name":"sign","probability":0.795149803161621},{"tag_name":"photo","probability":0.0147841582074761},{"tag_name":"fire","probability":0.0184208210557699},{"tag_name":"police","probability":0.0153429144993424},{"tag_name":"children","probability":0.00931504089385271},{"tag_name":"group_20","probability":0.683478415012359},{"tag_name":"group_100","probability":0.207240253686904},{"tag_name":"flag","probability":0.122076518833637},{"tag_name":"night","probability":0.212110564112663},{"tag_name":"shouting","probability":0.0291868895292282}]}}',
                buttonWord:"开始检测",
                imageName:"",
                showPercent:"概率：1.75%",
                isForce:false,
                imageRight:false,
                imageIsBig:false,
                activeName: 'first',
                showJson :{},
                options:{background:"rgba(0, 0, 0, 0.3)",fullscreen:false,target:document.querySelector(".show_json_outer")},
                currentImage:1,
                isLoading:false,
                clickFirst:0,
                fileList: [],
				isImage:false,
                imgUrl1:require('../../static/imgs/usage_image1.png'),
                imgUrl2:require('../../static/imgs/usage_image2.png'),
                imgUrl3:require('../../static/imgs/usage_image03.png'),
                recommendedList:[{'imgUrl':"../../static/imgs/usage_image1.png"},{'imgUrl':'../../static/imgs/usage_image2.png'},{'imgUrl':'../../static/imgs/usage_image03.png'}],
            	introduceList:[
            	    {'src':'../../static/imgs/word1.png','title':'身份证识别','des':'对二代居民身份证正反两面全部字段的结构化识别，能够满足身份证使用场景中对任意字段的识别需求'},
                    {'src':'../../static/imgs/word4.png','title':'通用识别','des':'能够快速准确识别各种网络图片中的文字，在复杂字体 和复杂背景的情况下仍能保持非常高的识别准确率'},
            	    {'src':'../../static/imgs/word2.png','title':'行驶证识别','des':'对机动车行驶证主页及副页所有21个字段进行结构化识别'},
            	    {'src':'../../static/imgs/word3.png','title':'驾驶证识别','des':'支持对机动车驾驶证正本所有9个字段进行结构化识别，包括证号、姓名、性别、国籍、住址、出生日期等 '},
            	    {'src':'../../static/imgs/word5.png','title':'营业执照识别','des':'对营业执照的注册号、社会信用代码、单位名称、法人、住址、有效期进行结构化识别'},
            	    {'src':'../../static/imgs/word6.png','title':'银行卡识别','des':'对银行卡的卡号、有效期、发卡行、卡片类型进行结构化识别'},
            	    {'src':'../../static/imgs/word7.png','title':'手写体识别','des':'支持对图片中的手写中文、手写数字进行检测和识别，针对不规则的手写字体进行专项优化，识别准确率高'},
            	    {'src':'../../static/imgs/word8.png','title':'车牌识别','des':'支持对中国大陆机动车车牌的识别，包括地域编号和车牌号'},
            	    {'src':'../../static/imgs/word9.png','title':'名片识别','des':'对各类名片的姓名、公司、职位、邮编、邮箱、电话、网址、地址、手机号进行结构化识别 '},
				]
			}
        },
        mounted:function () {

        },
        methods: {
            uploadInfo(response){
                var result = response.result;
                console.log( result.data.tag_list[1].probability,"hhhhhhhhhhhh") ;
                var jdata = JSON.stringify(result, null, 4);
                $("#show_json").html("<pre>"+jdata+"</pre>");//这时数据展示正确
                var forcePercent = result.data.tag_list[1].probability.toString();
                forcePercent = forcePercent.substring(0,forcePercent.indexOf(".")+5)*100;
                console.log(forcePercent);
                this.showPercent =`概率：${forcePercent}%`;

                if(forcePercent>80){
                    this.isForce = true;
                }
            },
            onImageChange(file, fileList){
               this.fileList.push(file);
               this.isImage = true;
			},
            changeImage(e){

                this.imageIsBig = false;
                this.imageRight = false;
                var file = e.target.files[0]
                var reader = new FileReader()
                var that = this
                reader.readAsDataURL(file);
                this.imageName = file.name;
                reader.onload = function(e) {
                    that.dialogImageUrl = this.result
                }
                let size=file.size;//文件的大小，判断图片的大小
                debugger;
                if(size>1048576){
                    this.imageIsBig = true;
                }else {
                    this.imageRight = true;
                }
            },
            clickImage(index){
                if(index!=this.currentImage){
                    this.currentImage =index;
                    this.dialogImageUrl = require(`../assets/image/yellow//y-${index}.jpg`);
                    if(this.clickFirst===0){
                        this.loadDate();
                    }
                }
            },
            loadDate() {
                this.isLoading = true;
                $(".show_sm_image").attr("disabled",true).css("pointer-events","none");
                console.log(this.clickFirst)
                if(this.clickFirst===0){
                    this.isLoading = true;
                    this.clickFirst+=1;
                    $("#show_json").html("");//这时数据展示正确
                    var intervalid1 = setTimeout(() => {
                        var jdata = JSON.stringify(JSON.parse(this.jsonDemo), null, 4);
                        $("#show_json").html("<pre>"+jdata+"</pre>");//这时数据展示正确
                        clearInterval(intervalid1);
                        this.isLoading = false;
                        $(".show_sm_image").attr("disabled",false).css("pointer-events","auto");
                        this.clickFirst = 0;
                    }, 4000)
                }

            },
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },
            handlePictureCardPreview(file) {
                this.dialogImageUrl = file.url;
                this.dialogVisible = true;
            },
            toPractice(){
                scrollBy(document.getElementById('practice_title').offsetTop-100);
//                window.scrollBy(0,document.getElementById('practice_title').offsetTop-100)
            }
        },
		components:{
            Navigation,
            FooterIndex
		},

    }

</script>

<style scoped>
	.word_top_contain{font-size: 0;line-height: 0;}
	.banner_outer{position: relative;}
	.describe_outer_banner{position: absolute;top:25%;font-size: 16px;color: white;width: 28%;height: 75%;}
	.describe_outer_banner p{}
	.describe_outer_banner p:nth-of-type(1){font-size: 30px;height: 60px;line-height: 60px;margin-bottom: 15px;min-width: 400px;}
	.describe_outer_banner p:nth-of-type(2){height: 130px;text-align: justify;overflow: hidden;min-width: 600px;line-height: 30px;}
	.word_top_contain img{height: 480px;min-width: 1300px;}
	.word_top_contain .banner_outer{background-image: url('../assets/image/word/word_banner.png');min-width: 1300px;}
	.practice_online{height: 40px;line-height:40px;width: 135px;font-size: 15px;text-align: center;color: #fff;border: 1px solid #fff;cursor:pointer}
	.practice_online:hover{background-color: white;color: #000;}

	.functional_introduce .title{text-align: center;color: #000;font-size: 30px;margin: 10px 0 40px;}
	.functional_introduce{padding: 50px 0;background-color: #f4f5f7;}
	.functional_experience{margin: 50px 0;background-color: #fff;}
	.functional_experience .title{text-align: center;color: #000;margin: 40px 0 15px;font-size: 30px;}
	.functional_experience .title_describe{text-align: center;color: #000;font-size: 14px;width: 70%;margin: 0 auto 30px;}
	.show_nav{width: 100%;margin: 0 auto;}
	.show_nav ul{margin:30px 0;display: flex;border-bottom: 1px solid #e2ecfc;}
	/*.show_nav ul li{height:36px;float:left;flex: 1;overflow: hidden;padding-bottom: 10px;}*/
	.show_nav ul li{height:36px;width: 120px;overflow: hidden;padding-bottom: 10px;}
	.show_nav ul li a{height:36px;line-height:36px;font-size:16px;color:#666;display:block;text-align: center;padding-bottom: 8px;}
	.show_nav ul li a.active{color:#316dff;border-bottom:2px solid #316dff;}
	.show_nav ul li a:hover{color:#316dff;}

	.word_introduce_outer{margin-bottom: 15px;text-align: center;min-width: 800px;}
	.word_introduce_outer ul{width: 100%;line-height: 0;font-size: 0;}
	.word_introduce_outer ul li{width: 31.7%;margin-right: 2.45%;margin-bottom: 2.45%;}
	.word_introduce_outer ul li:nth-of-type(3n){margin-right: 0;}
	.word_introduce_outer .describe_image_outer{height: 220px;overflow: hidden;}
	.word_introduce_outer li img{width: 100%;min-height: 220px;}
	.word_introduce_outer .introduce_describe_outer{height: 145px;background-color: #fff;padding: 0 30px;overflow: hidden;}
	.word_introduce_outer .introduce_describe_outer p{font-size: 18px;text-align: center;line-height: 60px;color: #000000;}
	.word_introduce_outer .introduce_describe_outer span{display:inline-block;font-size: 14px;text-align: left;line-height: 25px;color: #999999;padding-bottom: 10px;}


	.advantage_product{padding: 65px 0 80px ;overflow: hidden;background-color: #f2f2f5;}
	.advantage_product .title{text-align: center;color: #000000;margin: 10px 0;font-size: 30px;}
	.advantage_product span{display: inline-block;padding: 10px;}
	.title_image_common{width: 70px; height: 70px;display: inline-block;margin-top: 50px;background-size: 70px 70px;}
	.title_image{background-image: url("../assets/image/yellow/yellow_advantage1.png");}
	.title_image_two{background-image: url("../assets/image/yellow/yellow_advantage2.png");}
	.title_image_three{background-image: url("../assets/image/yellow/yellow_advantage3.png");}
	.good_describe{font-size: 16px;color: #666666;line-height: 25px;text-align: center;}
	.describe_outer{width: 90%;margin: 0 auto;text-align: left}
	.show_advantage_describe{padding: 14px;}
	.show_advantage_describe span{font-size: 24px;color: #333333;}


	.recommended_scenario{padding: 50px 0 200px;overflow: hidden;background-color: #fff;}
	.recommended_scenario .title{text-align: center;color: #000000;margin: 50px 0;font-size: 30px;}
	.recommended_scenario ul{display: flex;}
	.recommended_scenario ul li{flex: 1;height: 300px;margin-right: 30px;padding: 0 20px;color: #ffffff;text-align: justify;background-size: 100% 100%;}
	.recommended_scenario ul li p{margin-top: 30px;height: 60px;line-height: 60px;font-size: 18px;text-align: center;}
	.recommended_scenario ul li span{display: inline-block;line-height: 40px;font-size: 14px;}
	.recommended_scenario ul li:nth-of-type(1){background-image: url("../assets/image/ocr/word_scene_image1.png");}
	.recommended_scenario ul li:nth-of-type(2){background-image: url("../assets/image/ocr/word_scene_image2.png");}
	.recommended_scenario ul li:nth-of-type(3){background-image: url("../assets/image/ocr/word_scene_image3.png");margin-right: 0;}


</style>