<template>
	<div id="voiceRecognition">
		<Navigation></Navigation>
		<div class="voice_top_contain">
			<el-row>
				<el-row>
					<el-col :xl={span:24}>
						<div class="banner_outer ai-common-banner">
							<!--<img src="../assets/image/voice/voice_banner.png" alt="">-->
							<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
								<div class="describe_outer_banner">
									<p class="ell">语音识别</p>
									<p class="ell-rows-4 ">依托南海云的语音识别技术，为您提供高精度的语音转文字功能，支持多场景多领域的识别，可为社交聊天、智能家居、游戏娱乐等行业提供语音解决方案；结合敏感词检测技术节省审核人力，规避违规风险。</p>
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
						<p class="title_describe">业内领先的语音识别技术，结合敏感词检测过滤规则体系，精准、高效分析识别违规音频</p>
						<div class="introduce_outer">
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_one left_image_con"></span>
								<div class="right_word_con fl">
									<span>准确识别语音</span>
									<div class="scenario_describe_outer">
										<span class="good_describe">采用领先国际的方法，结合中文语义理解智能纠错，近场中文普通话识别准确率达98%</span>
									</div>
								</div>
							</div>
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_two left_image_con"></span>
								<div class="right_word_con fl">
									<span>快速高效识别 </span>
									<div class="scenario_describe_outer">
										<span class="good_describe">采用最新解码技术，API接口识别速度提升5倍以上，耗时仅音频时长十分之一，提升语音交互体验 </span>
									</div>
								</div>
							</div>
						</div>
						<div class="introduce_outer">
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_three left_image_con"></span>
								<div class="right_word_con fl">
									<span>支持自定义优化 </span>
									<div class="scenario_describe_outer">
										<span class="good_describe">可通过上传自定义词条进行训练，持续优化特定词条的识别效果，提升特定行业或业务场景的准确率 </span>
									</div>
								</div>
							</div>
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_four left_image_con"></span>
								<div class="right_word_con fl">
									<span>智能中文标点 </span>
									<div class="scenario_describe_outer">
										<span class="good_describe"> 根据语音的内容理解和停顿匹配标点符号（，。！？），使识别结果的表现方式贴合表述，更加可懂 </span>
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
						<div class="item_outer">
							<div class="voice_content">
								<p class="voice_title">语音识别</p>
								<!--<div class="language_select_outer">
									<span>语种/方言:</span>
									<select name="language" id="language" readonly="readonly">
										<option value="中文普通话">中文普通话</option>
										&lt;!&ndash;<option value="英文">英文</option>&ndash;&gt;
									</select>
								</div>-->
								<p class="suggest_record" v-show="recordWord =='开始录音'">语音识别支持中文普通话，先录音再识别</p>
								<div class="voice_time_outer" v-show="recordWord =='停止录音'">
									<img src="../assets/image/voice/voice.gif" alt="">
									<span>00:{{voiceSecond}}/01:00</span>
								</div>
							</div>
							<div class="voice_content">
								<p class="voice_title">识别结果</p>
								<textarea class="result_text" readonly="readonly">{{showResult}}</textarea>
							</div>
						</div>
						<p class="begin_record_time" v-if="toShort">{{recordWord}}</p>
						<p class="begin_record" @click="beginRecord" v-else>{{recordWord}}</p>
					</div>

				</el-col>
			</el-row>

		</div>

		<div class="recommended_scenario">
			<p class="title">应用场景</p>

			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
					<ul>
						<li>
							<p>实时字幕</p>
							<span>将直播、视频、现场演讲等音频进行实时的字幕转换，降低理解成本，提升用户体验 </span>
						</li>
						<li>
							<p>游戏娱乐</p>
							<span>语音聊天转文字，让用户在操作的同时也可看到聊天内容 </span>
						</li>
						<li>
							<p>语音搜索</p>
							<span>语音聊天转文字，让用户在操作的同时也可看到聊天内容</span>
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
									<p class="good_describe">领先的中文语音识别转写技术，普通话转写准确率可达95%以上</p>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_two title_image_common"></i>
							<div class="show_advantage_describe">
								<span>及时高效</span>
								<div class="describe_outer">
									<p class="good_describe">基于用户语音特征，建立个性化的词条语言模 型，调整识别参数，持续优化识别效果。</p>
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
    import Recorder,{ ENCODE_TYPE } from 'recorderx';
    export default {
        data() {
			return{
                buttonWord:"开始检测",
                options:{background:"rgba(0, 0, 0, 0.3)",fullscreen:false,target:document.querySelector(".show_json_outer")},
                isLoading:false,
                recommendedList:[{'imgUrl':"../../static/imgs/usage_image1.png"},{'imgUrl':'../../static/imgs/usage_image2.png'},{'imgUrl':'../../static/imgs/usage_image03.png'}],
                voiceSecond:'00',
                recordWord:'开始录音',
                intervalId:null,
                record:null,
                recordSrc:require("../assets/audio/1.mp3"),
				showResult:"",
				toShort:false

			}
        },
        mounted:function () {

        },
        methods: {
            beginRecord(){
				if(this.recordWord =="停止录音"){
                    this.recordStop();
                    clearInterval(this.intervalId) ;
				}else{
                    this.recordWord ="停止录音";
                    this.showResult ='';
					this.voiceSecond="00";
                    this.recordStart();
                    this.toShort = true;
                    var intervalId =  setInterval(()=>{
                        this.voiceSecond++
                        this.voiceSecond = this.voiceSecond<10?'0'+this.voiceSecond:this.voiceSecond;
                        if(this.voiceSecond==60){
                            this.recordStop();
                            clearInterval(intervalId) ;
//                            this.recordWord ="重新录音";
                        }
                    },1000);
					this.intervalId = intervalId;
					let timeout = setTimeout(()=>{
                        this.toShort = false;
                        clearTimeout(timeout);
                    },1000)
				}

			},
            recordStart(){
                this.record = new Recorder(true);
//                this.record.start();
                this.record.start()
                    .then(() => {
                        console.log("start recording");
                    })
                    .catch(error => {
                        console.log("Recording failed.", error);
                    });
            },
            recordStop() {
                this.record.pause();
                var wav = this.record.getRecord({
                    encodeTo: ENCODE_TYPE.WAV,
                });
                console.log(wav);
                this.recordSrc =URL.createObjectURL(wav) ;
                let files = new window.File([wav], '1.wav', {type: 'audio/wav'});
//                this.recordSrc =wav ;
                console.log(this.recordSrc);
				this.record.clear();
                this.recordWord ="正在识别...";
                this.submitVoice(files);
//                document.getElementsByTagName('audio')[0].load();

            },
            submitVoice(wav){
                var loading = this.$loading({fullscreen:false,target:document.querySelector(".voice_content")});
                this.showResult = '';
                this.recordWord ="正在识别...";
                this.toShort = true;
                this.isCheck = 2;
                var formData = new FormData();
                formData.append('speech', wav);

                $.ajax({
                    url: this.api+"/api/v1/audio/get_chinese_speech/",
                    type: "post",
                    data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                    cache: false,
                    contentType: false,
                    processData: false,
                    success:(response)=>{
                        loading.close();
                        console.log(response);
                        if(response.data.text==''){
                            this.showResult =  "没有识别到内容，请重新录音...";
						}else {
                            this.showResult =  response.data.text;
						}
                        this.toShort = false;
                        this.recordWord ="重新录音";
                    },
                    error:()=>{
                        loading.close();
                        this.isCheck = 3;
                        this.toShort = false;
                        this.recordWord ="重新录音";
                        this.$message.error('上传失败，请重新上传！');
                    }
                });
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
	.voice_top_contain{font-size: 0;line-height: 0;}
	.banner_outer{position: relative;}
	.describe_outer_banner{position: absolute;top:25%;font-size: 16px;color: white;width: 28%;height: 85%;}
	.describe_outer_banner p{}
	.describe_outer_banner p:nth-of-type(1){font-size: 30px;height: 60px;line-height: 60px;margin-bottom: 15px;min-width: 400px;}
	.describe_outer_banner p:nth-of-type(2){height: 120px;text-align: justify;overflow: hidden;min-width: 550px;line-height: 30px;}
	.voice_top_contain img{height: 480px;min-width: 1300px;}
	.voice_top_contain .banner_outer{background-image: url('../assets/image/voice/voice_banner.png');min-width: 1300px;}
	.practice_online{height: 40px;line-height:40px;width: 135px;font-size: 15px;text-align: center;color: #fff;border: 1px solid #fff;cursor:pointer}
	.practice_online:hover{background-color: white;color: #000;}

	.functional_introduce .title{text-align: center;color: #000;font-size: 30px;margin: 10px 0 30px;}
	.functional_introduce{padding: 50px 0;background-color: #ffffff;min-width: 800px;}
	.functional_introduce .title_describe{text-align: center;color: #000;font-size: 14px;width: 70%;margin: 0 auto 30px;}
	.functional_introduce .introduce_outer{display: flex;}
	.functional_introduce .introduce_outer>div:nth-of-type(2){margin-right: 0;}
	.show_scenario_outer{height: 130px;flex: 1;border: 1px solid #e9ecf2;margin-top: 20px;margin-right: 40px;display: flex;}
	.left_image_con_one{background: url("../assets/image/voice/voice_introduce1.png") no-repeat center center;}
	.left_image_con_two{background: url("../assets/image/voice/voice_introduce2.png") no-repeat center center;}
	.left_image_con_three{background: url("../assets/image/voice/voice_introduce3.png") no-repeat center center;}
	.left_image_con_four{background: url("../assets/image/voice/voice_introduce4.png") no-repeat center center;}
	.left_image_con{display:inline-block;margin-left: 15px;height: 130px;padding: 0 60px;}
	.right_word_con{flex: 1;min-height: 80px;margin: auto 0 auto 10px;}
	.right_word_con>span{display: inline-block;color: #333333;font-size: 18px;height: 30px;line-height: 30px;margin-bottom: 10px;}
	.scenario_describe_outer{text-align: left;padding-right: 10px;}

	.functional_experience{margin: 50px 0;background-color: #fff;min-width: 800px;}
	.functional_experience .title{text-align: center;color: #000;margin: 40px 0 15px;font-size: 30px;}
	.functional_experience .voice_experience_outer{height: 415px;border: 2px dashed #acc3ff;margin-top: 50px;padding: 20px;background-color: #fbfcff;}
	.functional_experience .voice_experience_outer .item_outer{display: flex;}
	.functional_experience .voice_experience_outer .item_outer .voice_content{height: 310px;flex: 1;margin-right: 20px;border: 1px solid #e2ecfc;background-color: #ffffff;}
	.functional_experience .voice_experience_outer .item_outer .voice_content:nth-of-type(2){margin-right: 0;}
	.functional_experience  .voice_title{height: 30px;line-height:25px;width: 140px;background: url("../assets/image/voice/voice_title_back.png") no-repeat center;
		font-size: 14px;text-align: center;margin: -1px auto 0;color: #316dff;}
	.functional_experience .language_select_outer{width: 170px;margin: 30px auto;}
	.functional_experience .language_select_outer >span{font-size: 14px;color: #000000;}
	.suggest_record{text-align: center;font-size: 14px;color: #000;margin-top: 100px;}/*原来是40*/
	.language_select_outer #language{width:90px;height: 30px ;font-size: 12px;text-align: center;padding-left: 7px;  line-height: 30px;border: 1px solid #b6b6b6;border-radius: 5px;background:url("../assets/image/voice/select_back.png") no-repeat 72px center;}
	.voice_time_outer{height: 40px;line-height: 0;font-size: 0;text-align: center;margin-top: 115px;}/*原来是75*/
	.voice_time_outer>span{display:inline-block;height: 40px;line-height: 40px;font-size: 14px;vertical-align: middle;margin-left: 20px;}
	.voice_time_outer>img{height: 40px;line-height: 40px;vertical-align: middle}
	.result_text{margin: 10px 0;padding: 0 20px;;width: 100%;height: 80%;box-sizing: border-box;line-height: 25px;font-size: 14px;color: #000;}
	.begin_record{height: 45px;width: 160px;line-height: 45px;background-color: #316dff;color: #fff;margin: 40px auto;font-size: 16px;text-align: center;cursor: pointer;}
	.begin_record_time{height: 45px;width: 160px;line-height: 45px;background-color: #f5f5f5;color: #666;margin: 40px auto;font-size: 16px;text-align: center;cursor: pointer;}
	.begin_record:hover{background-color: #6087F7;}

	.voice_introduce_outer{margin-bottom: 15px;text-align: center;min-width: 800px;}
	.voice_introduce_outer ul{width: 100%;line-height: 0;font-size: 0;}
	.voice_introduce_outer ul li{width: 32%;margin-right: 2%;margin-bottom: 20px;}
	.voice_introduce_outer ul li:nth-of-type(3n){margin-right: 0;}
	.voice_introduce_outer .describe_image_outer{height: 220px;overflow: hidden;}
	.voice_introduce_outer li img{width: 100%;min-height: 220px;}
	.voice_introduce_outer .introduce_describe_outer{min-height: 145px;background-color: #fff;padding: 0 30px;}
	.voice_introduce_outer .introduce_describe_outer p{font-size: 18px;text-align: center;line-height: 60px;color: #000000;}
	.voice_introduce_outer .introduce_describe_outer span{display:inline-block;font-size: 14px;text-align: left;line-height: 25px;color: #999999;padding-bottom: 10px;}


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


	.recommended_scenario{padding: 50px 0 200px;overflow: hidden;background-color: #fff;min-width: 1200px;}
	.recommended_scenario .title{text-align: center;color: #000000;margin: 50px 0;font-size: 30px;}
	.recommended_scenario ul{display: flex;}
	.recommended_scenario ul li{width: 380px;height: 340px;margin-right: 30px;padding: 0 65px;color: #ffffff;text-align: justify;background-size: 100% 100%;}
	.recommended_scenario ul li p{margin-top: 95px;height: 60px;line-height: 60px;font-size: 24px;text-align: center;}
	.recommended_scenario ul li span{display: inline-block;line-height: 25px;font-size: 14px;text-align: center;}
	.recommended_scenario ul li:nth-of-type(1){background-image: url("../assets/image/voice/voice_scence1.png");}
	.recommended_scenario ul li:nth-of-type(2){background-image: url("../assets/image/voice/voice_scence2.png");}
	.recommended_scenario ul li:nth-of-type(3){background-image: url("../assets/image/voice/voice_scence3.png");margin-right: 0;}


</style>