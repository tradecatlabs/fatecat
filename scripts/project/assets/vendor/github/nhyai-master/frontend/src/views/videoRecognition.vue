<template>
	<div id="videoRecognition">
		<Navigation></Navigation>
		<div class="video_top_contain">
			<el-row>
				<el-row>
					<el-col :xl={span:24}>
						<div class="banner_outer ai-common-banner">
							<!--<img src="../assets/image/video/video_banner.png" alt="">-->
							<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:16,offset:4}>
								<div class="describe_outer_banner">
									<p class="ell">视频检测</p>
									<p class="ell-rows-4 ">针对视频内容进行多维智能审核，其中包括色情、暴恐、政治敏感、民谣、自定义黑库等，让您的平台免去审核的后顾之忧 </p>
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
					<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:18,offset:3} :lg={span:18,offset:3} :xl={span:14,offset:5}>
						<p class="title_describe">对视频中的语音、文字、图像进行多维检测，及时发现涉黄、涉暴、政治敏感、民谣、
							违禁品等风险内容同时支持自定义视频黑库，基于视频指纹技术实现视频对比。识别准确率高，实时跟进最新政策，大幅减少人工审核 </p>
						<div class="introduce_outer">
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_one left_image_con"></span>
								<div class="right_word_con fl">
									<span>色情视频识别</span>
									<div class="scenario_describe_outer ell-rows-2">
										<span class="good_describe">基于海量大数据样本库，领先机器学习算法，高效识别涉黄视频</span>
									</div>
								</div>
							</div>
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_two left_image_con"></span>
								<div class="right_word_con fl">
									<span>暴恐视频识别 </span>
									<div class="scenario_describe_outer ell-rows-2">
										<span class="good_describe">海量大数据样本库，辅助业务安全数据监控，高效识别暴恐视频 </span>
									</div>
								</div>
							</div>
						</div>
						<div class="introduce_outer">
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_three left_image_con"></span>
								<div class="right_word_con fl">
									<span>政治敏感识别 </span>
									<div class="scenario_describe_outer ell-rows-2">
										<span class="good_describe">共享大数据样本库，政策法规权威同步，高效过滤涉政视频 </span>
									</div>
								</div>
							</div>
							<div class="clearfix show_scenario_outer">
								<span class="fl left_image_con_four left_image_con"></span>
								<div class="right_word_con fl">
									<span>自定义视频黑库 </span>
									<div class="scenario_describe_outer ell-rows-2">
										<span class="good_describe"> 共享违禁MD5视频公库，实时拦截违规视频，支持自定义添加私库  </span>
									</div>
								</div>
							</div>
						</div>
					</el-col>
				</el-row>
		</div>
		<div class="functional_experience" id="practice_title">
			<p class="title">功能体验</p>
			<!--初始化效果-->
			<div v-show="!isChose">
				<el-row style="min-width: 800px;margin-top: 30px;">
					<el-col :md={span:18,offset:3} :lg={span:18,offset:3} :xl={span:14,offset:5}>
						<div class="video_original">
							<div>
								<img src="../assets/image/video/video_play_logo.png" alt="">
								<p>支持视频格式：mp4，大小限制<20M</p>
								<div class="local_upload">
									<!--<p>本地上传</p>-->
									<input id="datafile" name="datafile" type="file" accept="video/mp4" class="inputfile" @change="changeImage($event)">
									<label for="datafile">开始选择</label>
								</div>
							</div>
						</div>
					</el-col>
				</el-row>
			</div>

			<!--视频评审-->
			<div v-show="isChose">
				<el-row style="min-width: 800px;margin-top: 30px;">
					<el-col :md={span:10,offset:3} :lg={span:12,offset:3} :xl={span:10,offset:5}><!--element-loading-text="拼命加载中"-->
						<div class="show_video_outer"
							 element-loading-background="rgba(0, 0, 0, 0.3)"
							 v-loading="isLoading">
							<div class="show_video">
								<!--<video id="video" :src="videoUrl" controls style="height: 100%;width: 100%;background-color: #333333"></video>-->
								<video id="myVideo" class="video-js vjs-defalut-skin" controls preload="metadata" :src="videoUrl.url">
									<source :src="videoUrl.url" type="video/mp4">
									<!--<source src="" type="video/mp4">-->
									您的浏览器不支持视频
								</video>

							</div>
						</div>
						<el-progress  :text-inside="true" :percentage="percentage" :stroke-width="3"></el-progress>
					</el-col>
					<el-col :md="8" :lg="6" :xl="4">
						<div class="video_result_outer">
							<p class="result_title">审查结果</p>
							<div class="result_outer">
								<p>暴恐识别</p>
								<p class="green_style_name" v-if="forceInfo==200">识别中...</p>
								<p class="red_style_name" v-else-if="forceInfo==201">上传失败...</p>
								<p class="red_style_name" v-else-if="this.forceInfo>=80">违规</p>
								<p class="orange_style_name" v-else-if="50<this.forceInfo">疑似违规</p>
								<p class="green_style_name" v-else>合规</p>
							</div>
							<div class="result_outer">
								<p>色情识别</p>
								<p class="green_style_name" v-if="sexInfo==200">识别中...</p>
								<p class="red_style_name" v-else-if="sexInfo==201">上传失败...</p>
								<p class="red_style_name" v-else-if="this.sexInfo>=80">违规</p>
								<p class="orange_style_name" v-else-if="50<this.sexInfo">疑似违规</p>
								<p class="green_style_name" v-else>合规</p>
							</div>
							<!--<div class="result_outer">
								<p class="ell">政治敏感识别</p>
								<p class="green_style_name">合规</p>
							</div>-->
							<!--<div class="result_outer">
								<p>公众人物识别</p>
								<p class="red_style_name">违规</p>
							</div>
							<div class="result_outer">
								<p>广告检测</p>
								<p class="red_style_name">违规</p>
							</div>-->
						</div>
					</el-col>
				</el-row>
				<el-row style="min-width: 800px;">
					<el-col :md={span:18,offset:3} :lg={span:18,offset:3} :xl={span:14,offset:5}>
						<div class="video_image_outer">
							<p v-show="forceImageUrl.length" class="evidence_info">暴恐识别证据信息</p>
							<div class="video_image_con clearfix">
								<div class="video_image_item fl" v-for="(item,index) in forceImageUrl">
									<div class="show_result_title">
										<div></div>
										<span class="video_result_red_title" v-if="item.violence_sensitivity_level>80">违规</span>
										<span class="video_result_orange_title" v-else>疑似违规</span>
										<span class="video_result_red_number" v-if="item.violence_sensitivity_level>80">{{item.violence_sensitivity_level}}%</span>
										<span class="video_result_orange_number" v-else>{{item.violence_sensitivity_level}}%</span>
									</div>
									<img :src="item.image_url" alt="">
									<p>视频时间：{{item.sensitivity_time|secondToTime}}</p>
								</div>
							</div>
							<p v-show="sexImageUrl.length" class="evidence_info">色情识别证据信息</p>
							<div class="video_image_con clearfix">
								<div class="video_image_item fl" v-for="(item,index) in sexImageUrl">
									<div class="show_result_title">
										<div></div>
										<span class="video_result_red_title" v-if="item.porn_sensitivity_level>80">违规</span>
										<span class="video_result_orange_title" v-else>疑似违规</span>
										<span class="video_result_red_number" v-if="item.porn_sensitivity_level>80">{{item.porn_sensitivity_level}}%</span>
										<span class="video_result_orange_number" v-else>{{item.porn_sensitivity_level}}%</span>
									</div>
									<img :src="item.image_url" alt="">
									<p>视频时间：{{item.sensitivity_time|secondToTime}}</p>
								</div>
							</div>
							<div class="local_upload" v-if="!isLoading">
								<!--<p>本地上传</p>-->
								<input id="videofile" name="datafile" type="file" accept="video/mp4" class="inputfile" @change="changeImage($event)">
								<label for="datafile">重新选择</label>
							</div>
							<div class="local_upload" v-else>
								<p>重新选择</p>
							</div>
						</div>
						<p class="suggest"><span style="color: red">*</span> 提示: 敏感系数<50%为合规，50%～80%为疑似违规，>80%为违规<span v-show="imageIsBig" style="color: red;margin-left: 10px;display: inline-block;">！该图片大小超过1M</span></p>

					</el-col>
				</el-row>
			</div>
		</div>
		<div class="recommended_scenario">
			<p class="title">应用场景</p>
			<el-row>
				<el-col :xs={span:24} :sm={span:22,offset:1} :md={span:20,offset:2} :lg={span:18,offset:3} :xl={span:14,offset:5}>
					<ul>
						<li>
							<p>UGC短视频审核</p>
							<span>实时检测UGC短视频社区用户自主上传视频的违规内容</span>
						</li>
						<li>
							<p>点播视频</p>
							<span>高效识别点播视频中的违规色情、涉政类镜头 </span>
						</li>
						<li>
							<p>直播平台内容审核</p>
							<span>实时检测直播间内视频，支持截图过检和电视墙审核</span>
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
									<p class="good_describe">视频内容进行分析，提取特征，对色情、暴恐、政敏等识别准确率高</p>
								</div>
							</div>
						</el-col>
						<el-col :xs={span:24} :sm={span:12} :md={span:8} :lg={span:8} :xl={span:8} align="center" style="min-height: 250px;">
							<i class="title_image_two title_image_common"></i>
							<div class="show_advantage_describe">
								<span>及时高效</span>
								<div class="describe_outer">
									<p class="good_describe">24小时不间断服务，日审核图片过千万，可有效降低90%以上的人工审核成本。</p>
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
    import {secondToTime} from '../store/common'
    import { Message } from 'element-ui';
    export default {
        data() {
			return{
                buttonWord:"开始检测",
                options:{background:"rgba(0, 0, 0, 0.3)",fullscreen:false,target:document.querySelector(".show_video")},
                isLoading:false,
                recommendedList:[{'imgUrl':"../../static/imgs/usage_image1.png"},{'imgUrl':'../../static/imgs/usage_image2.png'},{'imgUrl':'../../static/imgs/usage_image03.png'}],
                voiceSecond:'00',
                recordWord:'开始录音',
                intervalId:null,
                isChose:false,
                videoUrl:{},
                imageIsBig:false,
				imageUrl:[],
				sexImageUrl:[],
				forceImageUrl:[],
				markerInfo:[],
				sexInfo:5,
				forceInfo:5,
                player:{},
                first:true,
                percentage:0
			}
        },
        mounted:function () {

        },
        methods: {
            format(percentage) {
                return percentage === 100 ? '满' : `${percentage}%`;
            },
            resetMarker(marker){
//                this.player = null;
                this.player = videojs('myVideo');
                var player = this.player;
				console.log(this.player);
                player.markers.reset(marker)
			},
            initVideo(item){
//                this.player = null;
                this.player = videojs('myVideo');
                console.log(this.player);
                var player = this.player;
                player.markers({
                    markerStyle:{  //标记样式
                        'width':'5px',
                        'border-radius': '5px',
                        /* 'background-color': 'red'*/
                    },
                    markerTip:{  //悬停标记提示对象
                        display:true,  //是否显示markerTips
                        /*
						  用于动态构建标记提示文本的回调函数。
						  只需返回一个字符串，参数标记是传递给插件的标记对象
						 */
                        text: function(marker) {
                            return  marker.text;
                        }
                    },
                    breakOverlay:{  //每个标记的中断覆盖选项
                        display: true,  //是否显示叠加层
                        displayTime: 3,
                        style:{  //为叠加层添加css样式
                            color:"red"
                        },
                        text: function(marker) {  //回调函数动态构建叠加文本
                            return  marker.text;
                        }
                    },
                    onMarkerReached:function(marker, index){  //只要播放到标记的时间间隔，就会出发此回调函数

                    },
                    onMarkerClick:function(marker,index){  //单击标记时会触发此回调函数，
                        /*
						  单击标记的默认行为是在视频中寻找该点，
						  但是，如果onMarkerClick返回false，则将阻止默认行为
						*/
                    },
                    markers:item,
                });
			},

            uploadImage(e,file,url){
                this.imageRight = false;
                this.sexInfo = 200;
                this.forceInfo = 200;
                this.imageUrl= [];
                this.sexImageUrl= [];
                this.forceImageUrl= [];
//                this.loading = this.$loading(this.options);
                this.isLoading= true;
                var formData = new FormData();
                formData.append('video', file);
                // formData.append('video_url', url);
                console.log(file,url);
                this.percentage= 0;
                var timer = window.setInterval(()=>{
                    this.percentage += 5;
                    if (this.percentage > 95) {
                        this.percentage = 95;
                    }
                },2000);
                $.ajax({
                    url: this.api+"/api/v1/video/get_video_inspection/",
                    type: "post",
                    data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                    cache: false,
                    timeout:3600000,
                    contentType: false,
                    processData: false,
                    success:(response)=>{
//                        this.$loading().close();
                        this.sexInfo= 5;
                        this.forceInfo= 5;
                        this.markerInfo= [];
                        this.percentage = 100;
                        window.clearInterval(timer);
						console.log(response);
//                        this.videoUrl={url:response.data.video} ;
//						this.video_url= response.data.video_url;
                        this.sexImageUrl = response.data.porn_evidence_information;
                        this.forceImageUrl = response.data.violence_evidence_information;
                        response.data.video_evidence_information.forEach((item,index)=>{
                            if(parseFloat(item.porn_sensitivity_level)>this.sexInfo){
                                this.sexInfo = parseFloat(item.porn_sensitivity_level);
							}
                            if(parseFloat(item.violence_sensitivity_level)>this.forceInfo){
                                this.forceInfo = parseFloat(item.violence_sensitivity_level);
                            }
                            if(parseFloat(item.porn_sensitivity_level)>parseFloat(item.violence_sensitivity_level)){
                                if(parseFloat(item.porn_sensitivity_level)>80){
                                    this.markerInfo.push({
                                        time:item.sensitivity_time-response.data.interval/2,
                                        text:"违规",
                                        class:"red_style"
                                    });
                                    /*this.imageUrl.push({
                                        image:item.image_url,
                                        time:secondToTime(item.sensitivity_time),
                                        number:item.porn_sensitivity_level,
                                        state:"违规"
                                    });*/
								}else if(50<=parseFloat(item.porn_sensitivity_level)<80) {
                                    this.markerInfo.push({
                                        time:item.sensitivity_time,
                                        text:"疑似违规",
                                        class:"orange_style"
                                    });
                                    /*this.imageUrl.push({
                                        image:item.image_url,
                                        time:secondToTime(item.sensitivity_time),
                                        number:item.porn_sensitivity_level,
                                        state:"疑似违规"
                                    });*/
								}
							}else {
                                if(parseFloat(item.violence_sensitivity_level)>80){
                                    this.markerInfo.push({
                                        time:item.sensitivity_time-response.data.interval/2,
                                        text:"违规",
                                        class:"red_style"
                                    });
                                   /* this.imageUrl.push({
                                        image:item.image_url,
                                        time:secondToTime(item.sensitivity_time),
                                        number:item.violence_sensitivity_level,
                                        state:"违规"
                                    });*/
                                }else if(50<=parseFloat(item.violence_sensitivity_level)<80){
                                    this.markerInfo.push({
                                        time:item.sensitivity_time-response.data.interval/2,
                                        text:"疑似违规",
                                        class:"orange_style"
                                    });
                                   /* this.imageUrl.push({
                                        image:item.image_url,
                                        time:secondToTime(item.sensitivity_time),
                                        number:item.violence_sensitivity_level,
                                        state:"疑似违规"
                                    });*/
                                }
							}
						});
                        if(this.first){
                            this.initVideo(this.markerInfo);
//                            this.resetMarker(this.markerInfo);
                            this.first = false;
						}else {
                            this.resetMarker(this.markerInfo);
						}
                        this.isLoading= false;
                    },
                    error:(error)=>{
                        this.showMessage('上传失败，请重新上传！');
                        this.isLoading= false;
                        this.percentage = 0;
                        this.forceInfo = 201;
                        this.sexInfo = 201;
                        window.clearInterval(timer);
                    }
                });
                e.preventDefault();
            },
			showMessage(msg){
                this.$message.error({
                    showClose: true,
                    message: msg,
                    type: 'error',
                    duration:0
                });
			},
            changeImage(e){
                Message.closeAll();
                this.player = null;
                this.imageIsBig = false;
                this.imageRight = false;
                const file = e.target.files[0];
                if(file.size>20971520){
                    this.$message.error('请上传小于20M的视频！');
//                    this.showMessage('请上传小于20M的视频！');
                    return;
				}
                console.log(file);
                const reader = new FileReader();
                const that = this;
                reader.readAsDataURL(file);
                var url = URL.createObjectURL(file);
                console.log(url);
                this.videoUrl={url:url};
                console.log(this.videoUrl);
                this.isChose=true;
                this.uploadImage(e,file,url);
                this.toPractice();
                document.getElementById("datafile").value=null;
            },
            toPractice(){
                scrollBy(document.getElementById('practice_title').offsetTop-100);
//                window.scrollBy(0,document.getElementById('practice_title').offsetTop-100)
            },
        },
		components:{
            Navigation,
            FooterIndex
		},

    }

</script>

<style scoped>
	@import "../assets/css/videojs.markers.css";
	@import "../assets/css/video-js.min.css";
	.video_top_contain{font-size: 0;line-height: 0;}
	.banner_outer{position: relative;}
	.describe_outer_banner{position: absolute;top:25%;font-size: 16px;color: white;width: 28%;height: 85%;}
	.describe_outer_banner p{}
	.describe_outer_banner p:nth-of-type(1){font-size: 30px;height: 60px;line-height: 60px;margin-bottom: 15px;min-width: 400px;}
	.describe_outer_banner p:nth-of-type(2){height: 120px;text-align: justify;overflow: hidden;min-width: 550px;line-height: 30px;}
	.video_top_contain img{height: 480px;min-width: 1300px;}
	.video_top_contain .banner_outer{background-image: url('../assets/image/video/video_banner.png');min-width: 1300px;}
	.practice_online{height: 40px;line-height:40px;width: 135px;font-size: 15px;text-align: center;color: #fff;border: 1px solid #fff;cursor:pointer}
	.practice_online:hover{background-color: white;color: #000;}

	.functional_introduce .title{text-align: center;color: #000;font-size: 30px;margin: 10px 0 30px;}
	.functional_introduce{padding: 50px 0;background-color: #ffffff;min-width: 800px;}
	.functional_introduce .title_describe{text-align: center;color: #000;font-size: 14px;width: 70%;margin: 0 auto 30px;line-height: 25px;}
	.functional_introduce .introduce_outer{display: flex;}
	.functional_introduce .introduce_outer>div:nth-of-type(2){margin-right: 0;}
	.show_scenario_outer{height: 130px;flex: 1;border: 1px solid #e9ecf2;margin-top: 20px;margin-right: 40px;display: flex;}
	.left_image_con_one{background: url("../assets/image/video/video_introduce1.png") no-repeat center center;}
	.left_image_con_two{background: url("../assets/image/video/video_introduce2.png") no-repeat center center;}
	.left_image_con_three{background: url("../assets/image/video/video_introduce3.png") no-repeat center center;}
	.left_image_con_four{background: url("../assets/image/video/video_introduce4.png") no-repeat center center;}
	.left_image_con{display:inline-block;margin-left: 15px;height: 130px;padding: 0 60px;}
	.right_word_con{flex: 1;min-height: 80px;margin: auto 0 auto 10px;overflow: hidden;}
	.right_word_con>span{display: inline-block;color: #333333;font-size: 18px;height: 30px;line-height: 30px;margin-bottom: 10px;}
	.scenario_describe_outer{text-align: left;padding-right: 10px;}

	.functional_experience{margin: 50px 0;background-color: #fff;min-width: 800px;}
	.functional_experience .title{text-align: center;color: #000;margin: 40px 0 15px;font-size: 30px;}
	.show_video_outer{}
	.show_video{height:440px;position: relative;overflow: hidden;}
	.show_video #myVideo{width: 100%;height: 440px;}
	/*初始化页面begin*/
	.video_original{height: 410px;border: 2px dashed #acc3ff;background-color: #fbfcff;padding: 20px;}
	.video_original>div{height: 100%;background-color: #ffffff;text-align: center;}
	.video_original>div img{margin-top: 110px;}
	.video_original>div p:nth-of-type(1){font-size: 14px;color: #333333;height: 40px;line-height: 40px;margin: 20px 0;}

	.inputfile{z-index: -11111;width: 0px;height:1px;opacity: 0;}
	.local_upload{height: 45px;line-height: 45px;font-size: 16px;margin: 40px auto;text-align: center;}
	.local_upload label{display:inline-block;color: #ffffff;font-size: 16px;height: 42px;width: 120px;line-height: 42px;border: 1px solid #e1e3e7;text-align: center;background-color: #316dff;cursor: pointer;}
	.local_upload label:hover{background-color: #6087F7;color: white;}
	.local_upload p{display:inline-block;color: #666666;font-size: 16px;height: 42px;width: 120px;line-height: 42px;border: 1px solid #e1e3e7;text-align: center;background-color: #dddddd;cursor: pointer;}
	/*初始化页面end*/

	.video_result_outer{height: 440px;z-index: 99;background-color: white;box-shadow:5px 0 20px #c5cff1}
	.video_result_outer .result_title{font-size: 24px;color: #000000;text-align: center;height: 100px;padding-top: 30px;}
	.video_result_outer .result_title:before{content: "";background: url("../assets/image/result_top_image.png") no-repeat center center;height: 23px;display: block;margin-bottom: 10px;}
	.video_image_outer{border: 1px solid #e2ecfc;min-height: 200px;margin-top: 20px;padding-left: 20px;}
	.video_image_outer:first-child{color: #010101;font-size: 16px;line-height: 50px;}
	.evidence_info{height: 80px;line-height: 80px;font-size: 16px;}
	.video_image_item{height: 150px;width: 160px;padding-right: 20px;margin-bottom: 20px;position: relative;}
	.video_image_con .video_image_item img{height: 120px;width: 100%;display: block}
	.video_image_con .video_image_item p{height: 30px;line-height:30px;font-size: 14px;text-align: center;border: 1px solid #e2ecfc;border-top: none;}
	.show_result_title{position: absolute;height: 20px;font-size: 0;line-height: 0}
	.show_result_title span{;font-size: 14px;line-height: 20px;display: inline-block;vertical-align: top;}
	.show_result_title span:nth-of-type(2){background-color: white;padding: 0 5px;}
	.show_result_title span:nth-of-type(1){line-height: 22px;padding: 0 10px;}
	.video_result_red_number{color: #ff524a;border: 1px solid #ff524a;}
	.video_result_red_title{background-color: #ff524a;color: white;}
	.video_result_orange_number{color: #ffac09;border: 1px solid #ffac09;}
	.video_result_orange_title{background-color: #ffac09;color: white;}
	.choose_again{color: #ffffff;font-size: 16px;height: 42px;width: 120px;line-height: 42px;margin: 40px auto;border: 1px solid #e1e3e7;text-align: center;background-color: #316dff;cursor: pointer;}


	.show_json_outer .result_title{font-size: 24px;color: #000000;text-align: center;height: 100px;padding-top: 30px;}
	.show_json_outer .result_title:before{content: "";background: url("../assets/image/result_top_image.png") no-repeat center center;height: 23px;display: block;margin-bottom: 10px;}
	.suggest{color: #b2b2b2;font-size: 14px;min-height: 30px;margin:8px 0;}

	.result_outer{margin: 20px auto;display: flex;color: #000000;height: 28px;line-height: 28px;width: 210px;}
	.result_outer p:nth-of-type(1){font-size: 16px;width: 90px;}
	.result_outer p:nth-of-type(2){font-size: 16px;width: 120px;text-align: center}
	.result_outer p:nth-of-type(3){font-size: 16px;flex: 4;text-align: center}
	.result_outer .green_style_name{background-color: #54cd62;border: 1px solid #54cd62;color: #fff}
	.result_outer .orange_style_name{background-color: #ffac09;border: 1px solid #ffac09;color: #fff}
	.result_outer .red_style_name{background-color: #ff524a;border: 1px solid #ff524a;color: #fff}
	/*功能体验end*/

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
	.recommended_scenario ul li{flex: 1;height: 300px;margin-right: 20px;padding: 0 20px;color: #ffffff;text-align: justify;background-size: 100% 100%;}
	.recommended_scenario ul li p{margin-top: 70px;height: 60px;line-height: 60px;font-size: 18px;text-align: center;}
	.recommended_scenario ul li span{display: inline-block;line-height: 40px;font-size: 14px;text-align: center;}
	.recommended_scenario ul li:nth-of-type(1){background-image: url("../assets/image/video/video_scence1.png");}
	.recommended_scenario ul li:nth-of-type(2){background-image: url("../assets/image/video/video_scence2.png");}
	.recommended_scenario ul li:nth-of-type(3){background-image: url("../assets/image/video/video_scence3.png");margin-right: 0;}


</style>