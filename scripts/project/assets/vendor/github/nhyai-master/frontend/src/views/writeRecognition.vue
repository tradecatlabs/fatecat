<template>
	<div id="writeRecognition">
		<Navigation></Navigation>
		<div class="write_top_contain">
			<el-row>
				<el-row>
					<el-col :xl={span:24}>
						<div class="banner_outer ai-common-banner">
							<!--<img src="../assets/image/write/write_banner.png" alt="">-->
							<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
								<div class="describe_outer_banner">
									<p class="ell">敏感文字检测</p>
									<p class="ell-rows-4 ">基于海量样本数据，智能策略定制，高效过滤色情、民谣、涉政、暴恐等多类垃圾文字及敏感词、违禁变种</p>
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
				<el-row>
					<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
						<p class="title_describe">基于多年行业经验积累，针对文本垃圾特点，提供个性化匹配的模型，支持专属文本过滤方案定制</p>
						<div class="introduce_outer">
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_one left_image_con"></span>
								<div class="right_word_con fl">
									<span>色情文字识别</span>
									<div class="scenario_describe_outer">
										<span class="good_describe">结合语义分析和聚类分析，精准识别涉黄文本</span>
									</div>
								</div>
							</div>
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_two left_image_con"></span>
								<div class="right_word_con fl">
									<span>民谣类识别 </span>
									<div class="scenario_describe_outer">
										<span class="good_describe">结合大数据分析，快速识别谣言、诽谤、诋毁等民谣类文本</span>
									</div>
								</div>
							</div>
						</div>
						<div class="introduce_outer">
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_three left_image_con"></span>
								<div class="right_word_con fl">
									<span>违禁品识别 </span>
									<div class="scenario_describe_outer">
										<span class="good_describe">深度定制模型，建立多维度用户画像，高效识别宗教、枪支、血腥等违禁品</span>
									</div>
								</div>
							</div>
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_four left_image_con"></span>
								<div class="right_word_con fl">
									<span>涉政文字识别 </span>
									<div class="scenario_describe_outer">
										<span class="good_describe"> 实时共享违禁公库，支持自定义关键词，高效识别涉政文本 </span>
									</div>
								</div>
							</div>
						</div>
					</el-col>
				</el-row>
		</div>
		<div class="functional_experience" id="practice_title">
			<p class="title">功能体验</p>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<div class="voice_experience_outer">
						<div v-if="isCheck!=3" class="input_outer"  element-loading-background="rgba(0, 0, 0, 0.3)"
							  v-loading="isLoading">
							<textarea class="write_content" placeholder="输入或粘贴要检测的文字，不超过600字" id="orgAuditDesc" name="orgAuditDesc" v-model="recWord"></textarea>
						</div>
						<div id="show_result" v-else></div>
						<p class="word_more" id="text-count" v-show="isCheck==1">您还可输入600个字</p>
						<p v-show="isAgainst" class="against">{{againstWord}}</p>
						<p v-show="isPass" class="check_pass">通过（检测文本正常）</p>
						<p class="begin_record" @click="submitWord" v-if="isCheck==1">开始检测</p>
						<p class="again_record" v-if="isCheck==2">正在识别</p>
						<p class="again_record" @click="againWord" v-if="isCheck==3">再次检测</p>
					</div>
				</el-col>
			</el-row>

		</div>
		<div class="recommended_scenario">
			<p class="title">应用场景</p>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:14,offset:5}>
					<ul>
						<li>
							<p>视频、直播弹幕审核</p>
							<!--<span>将直播、视频、现场演讲等音频进行实时的字幕转换，降低理解成本，提升用户体验 </span>-->
						</li>
						<li>
							<p>用户原创内容审核</p>
							<!--<span>语音聊天转文字，让用户在操作的同时也可看到聊天内容 </span>-->
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
									<p class="good_describe">能够主动发现潜在的涉黄图片，打击精度高，覆盖广，响应快，第一时间遏制涉黄图片的传播</p>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_three title_image_common"></i>
							<div class="show_advantage_describe">
								<span>灵活性定制</span>
								<div class="describe_outer">
									<p class="good_describe">根据用户审核平台需求，深度定制产品策略与解决方案</p>
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
                buttonWord:"开始检测",
                options:{background:"rgba(0, 0, 0, 0.3)",fullscreen:false,target:document.querySelector(".show_json_outer")},
                recommendedList:[{'imgUrl':"../../static/imgs/usage_image1.png"},{'imgUrl':'../../static/imgs/usage_image2.png'},{'imgUrl':'../../static/imgs/usage_image03.png'}],
                voiceSecond:'00',
                recordWord:'开始识别',
                intervalId:null,
                recWord:'',
                isAgainst:false,
                isCheck:1,
                isLoading:false,
                isPass:false,
				againstWord:"违规（检测文本含有涉黄、涉政、涉爆、广告等违规信息）"
			}
        },
        mounted:function () {
            this.resetNumber();
        },
        methods: {
            resetNumber(){
                $('#orgAuditDesc').on('keyup',function() {
                    var txtval = $('#orgAuditDesc').val().length;
//							console.log(txtval);
                    var str = parseInt(600 - txtval);
//							console.log(str);
                    if (str > 0) {
                        $('#text-count').html('剩余可输入' + str + '字');
                    } else {
                        $('#text-count').html('剩余可输入0字');
                        $('#orgAuditDesc').val($('#orgAuditDesc').val().substring(0, 600)); //这里意思是当里面的文字小于等于0的时候，那么字数不能再增加，只能是600个字
                    }
                });
            },
            beginRecord(){
				if(this.recordWord =="停止录音"){
                    clearInterval(this.intervalId) ;
                    this.recordWord ="重新录音"
                    this.submitWord();
				}else{
                    this.voiceSecond="00";
                    var intervalId =  setInterval(()=>{
                        this.voiceSecond++
                        this.voiceSecond = this.voiceSecond<10?'0'+this.voiceSecond:this.voiceSecond;
                        this.recordWord ="停止录音";
                        if(this.voiceSecond==60){
                            clearInterval(intervalId) ;
                            this.recordWord ="重新录音"
                        }
                    },1000);
					this.intervalId = intervalId;
				}

			},
			submitWord(){
                if(this.recWord==''){
                    this.$message.error('请输入要识别的内容！');
                    return;
				}
				this.isCheck = 2;
                var formData = new FormData();
                formData.append('text', this.recWord);
                $.ajax({
                    url: this.api+"/api/v1/text/get_text_recognition/",
                    type: "post",
                    data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                    cache: false,
                    contentType: false,
                    processData: false,
                    success:(response)=>{
                        console.log(response);
                        this.isCheck = 3;
                        window.setTimeout(()=>{
                            document.getElementById('show_result').innerHTML= response.data.web_text;//msgsnew.join(',')
							const final = response.data.final_list.join('、');
							this.againstWord = `违规（检测文本含有${final}等违规信息）`;
                            if(response.ret==0){
                                this.isAgainst = true;
                            }else {
                                this.isPass = true
                            }
						},200);

//                        document.getElementsByClassName('write_content')[0].innerHTML=response.data.web_text;

//                        this.recWord =response.data.web_text;

                    },
                    error:()=>{
                        this.isCheck = 3;
                        this.$message.error('识别失败，请重新识别！');
					}
                });
			},
            againWord(){
                document.getElementById('show_result').innerHTML= "";
                this.isCheck = 1;
                this.recWord ="";
                this.isAgainst = false;
                this.isPass = false;
                window.setTimeout(()=>{
                    document.getElementById("orgAuditDesc").value="";
                    $('#text-count').html('剩余可输入600字');
                    this.resetNumber()
				},200)
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
	.write_top_contain{font-size: 0;line-height: 0;}
	.banner_outer{position: relative;}
	.describe_outer_banner{position: absolute;top:25%;font-size: 16px;color: white;width: 28%;height: 75%;}
	.describe_outer_banner p{}
	.describe_outer_banner p:nth-of-type(1){font-size: 30px;height: 60px;line-height: 60px;margin-bottom: 15px;min-width: 400px;}
	.describe_outer_banner p:nth-of-type(2){height: 105px;text-align: justify;overflow: hidden;min-width: 550px;line-height: 30px;}
	.write_top_contain img{height: 480px;min-width: 1300px;}
	.write_top_contain .banner_outer{background-image: url('../assets/image/write/write_banner.png');min-width: 1300px;}
	.practice_online{height: 40px;line-height:40px;width: 135px;font-size: 15px;text-align: center;color: #fff;border: 1px solid #fff;cursor:pointer}
	.practice_online:hover{background-color: white;color: #000;}

	.functional_introduce .title{text-align: center;color: #000;font-size: 30px;margin: 10px 0 30px;}
	.functional_introduce{padding: 50px 0;background-color: #ffffff;min-width: 800px;}
	.functional_introduce .title_describe{text-align: center;color: #000;font-size: 14px;width: 70%;margin: 0 auto 30px;}
	.functional_introduce .introduce_outer{display: flex;}
	.functional_introduce .introduce_outer>div:nth-of-type(2){margin-right: 0;}
	.show_scenario_outer{height: 130px;flex: 1;border: 1px solid #e9ecf2;margin-top: 20px;margin-right: 40px;display: flex;}
	.left_image_con_one{background: url("../assets/image/write/write_introduce1.png") no-repeat center center;}
	.left_image_con_two{background: url("../assets/image/write/write_introduce2.png") no-repeat center center;}
	.left_image_con_three{background: url("../assets/image/write/write_introduce3.png") no-repeat center center;}
	.left_image_con_four{background: url("../assets/image/write/write_introduce4.png") no-repeat center center;}
	.left_image_con{display:inline-block;margin-left: 15px;height: 130px;padding: 0 60px;}
	.right_word_con{flex: 1;min-height: 80px;margin: auto 0 auto 10px;}
	.right_word_con>span{display: inline-block;color: #333333;font-size: 18px;height: 30px;line-height: 30px;margin-bottom: 10px;}
	.scenario_describe_outer{text-align: left;padding-right: 10px;}

	.functional_experience{margin: 50px 0;background-color: #fff;min-width: 800px;}
	.functional_experience .title{text-align: center;color: #000;margin: 40px 0 15px;font-size: 30px;}
	.functional_experience .voice_experience_outer{height: 415px;border: 2px dashed #acc3ff;margin-top: 50px;padding: 20px;background-color: #fbfcff;position: relative;}
	.write_content{background-color: #ffffff;height: 305px;border: 1px solid #e2ecfc;width: 100%;color: #666666;font-size: 14px;padding: 10px;box-sizing: border-box;line-height: 26px;}
	#show_result{height: 300px;background-color: #ffffff;border: 1px solid #e2ecfc;padding: 10px;}
	.voice_experience_outer .against{text-align: center;color: #FE0808;font-size: 15px;margin-top: 10px;}
	.voice_experience_outer .check_pass{text-align: center;color: #333;font-size: 15px;margin-top: 10px;}
	.word_more{position: absolute;right: 40px;margin-top: -35px;font-size: 14px;color: #666666;}
	.begin_record{height: 45px;width: 160px;line-height: 45px;background-color: #316dff;color: #fff;margin: 20px auto;font-size: 16px;text-align: center;cursor:pointer;}
	.begin_record:hover{background-color: #6087F7;color: white;}
	.again_record{height: 45px;width: 160px;line-height: 45px;background-color: #FFFFFF;color: #333;margin: 20px auto;font-size: 16px;text-align: center;border: 1px solid #E7E9EC;cursor:pointer;}

	.advantage_product{padding: 65px 0 80px ;overflow: hidden;background-color: #f2f2f5;}
	.advantage_product .title{text-align: center;color: #000000;margin: 10px 0;font-size: 30px;}
	.advantage_product span{display: inline-block;padding: 10px;}
	.title_image_common{width: 70px; height: 70px;display: inline-block;margin-top: 50px;background-size: 70px 70px;}
	.title_image{background-image: url("../assets/image/yellow/yellow_advantage1.png");}
	.title_image_two{background-image: url("../assets/image/yellow/yellow_advantage2.png");}
	.title_image_three{background-image: url("../assets/image/yellow/yellow_advantage3.png");}
	.good_describe{font-size: 14px;color: #666666;line-height: 25px;text-align: center;}
	.describe_outer{width: 90%;margin: 0 auto;text-align: left}
	.show_advantage_describe{padding: 14px;}
	.show_advantage_describe span{font-size: 24px;color: #333333;}

	.recommended_scenario{padding: 50px 0 200px;overflow: hidden;background-color: #fff;}
	.recommended_scenario .title{text-align: center;color: #000000;margin: 50px 0;font-size: 30px;}
	.recommended_scenario ul{display: flex;}
	.recommended_scenario ul li{flex: 1;height: 340px;margin-right: 40px;padding: 0 20px;color: #ffffff;text-align: justify;background-size: 100% 100%;}
	.recommended_scenario ul li p{margin-top: 140px;height: 60px;line-height: 60px;font-size: 18px;text-align: center;}
	.recommended_scenario ul li span{display: inline-block;line-height: 40px;font-size: 14px;}
	.recommended_scenario ul li:nth-of-type(1){background-image: url("../assets/image/write/write_usage1.png");}
	.recommended_scenario ul li:nth-of-type(2){background-image: url("../assets/image/write/write_usage2.png");margin-right: 0;}
	.recommended_scenario ul li:nth-of-type(3){background-image: url("../assets/image/write/write_usage1.png");}


</style>