<template>
	<div class="videoCheck">
		<!--视频评审-->
		<div class="clearfix">
			<div class="show_video_outer fl">
				<div class="show_video">
					<video id="video" class="video-js vjs-defalut-skin" controls preload="metadata" :src="videoUrl.url">
						<source :src="videoUrl.url" type="video/mp4">
						<!--<source src="" type="video/mp4">-->
						您的浏览器不支持视频
					</video>
				</div>
				<el-progress  :text-inside="true" :percentage="percentage" :stroke-width="3"></el-progress>
			</div>
			<div class="video_result_outer fl">
				<p class="result_title">审查结果</p>
				<div class="result_outer">
					<p>暴恐识别</p>
					<p class="green_style_name" v-if="this.forceInfo==200">识别中...</p>
					<p class="red_style_name" v-else-if="forceInfo==201">上传失败...</p>
					<p class="red_style_name" v-else-if="this.forceInfo>=80">违规</p>
					<p class="orange_style_name" v-else-if="50<this.forceInfo">疑似违规</p>
					<p class="green_style_name" v-else>合规</p>
				</div>
				<div class="result_outer">
					<p>色情识别</p>
					<p class="green_style_name" v-if="this.sexInfo==200">识别中...</p>
					<p class="red_style_name" v-else-if="sexInfo==201">上传失败...</p>
					<p class="red_style_name" v-else-if="this.sexInfo>=80">违规</p>
					<p class="orange_style_name" v-else-if="50<this.sexInfo">疑似违规</p>
					<p class="green_style_name" v-else>合规</p>
				</div>
			</div>
		</div>
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
			<div class="local_upload_video" v-if="!isLoading">
				<!--<p>本地上传</p>-->
				<input id="inputVideo" name="inputVideo" type="file"  class="inputfile" @change="onChangeFile($event)">
				<label for="inputVideo">重新选择</label>
			</div>
			<p class="choose_again" v-else>重新选择</p>
		</div>
		<p class="suggest"><span style="color: red">*</span> 提示: 敏感系数<50%为合规，50%～80%为疑似违规，>80%为违规<span v-show="imageIsBig" style="color: red;margin-left: 10px;display: inline-block;">！该图片大小超过1M</span></p>

	</div>
</template>

<script>
    import {secondToTime} from '../../store/common'
    import { Message } from 'element-ui';
	export default {
        props:['stopVideo'],
	    data(){
	        return{
                imageIsBig:false,
                videoUrl:{},
                imageUrl:[],
                sexImageUrl:[],
                forceImageUrl:[],
                markerInfo:[],
                sexInfo:5,
                forceInfo:5,
                player:null,
                first:true,
                isLoading:false,
                percentage:0

			}
		},
		mounted(){

		},
        watch: {
            stopVideo:(newVal,oldVal) => {
                console.log(newVal);
                if(newVal){
                    var myVideo = document.getElementById("video");
                    console.log(myVideo);
                    if(myVideo.currentTime&myVideo.currentTime > 0){
                        myVideo.pause();
					}

                }
            }
        },

		methods:{
		    onChangeFile(e){
                this.$parent.changeImage(e);
			},
            submitVideo(e,file){
                this.isLoading = true;
                this.sexInfo = 200;
                this.forceInfo = 200;
                this.imageUrl=[];
                this.sexImageUrl= [];
                this.forceImageUrl= [];
                var url = URL.createObjectURL(file);
                console.log(url);
                this.videoUrl={url:url} ;
                console.log(file);
                this.percentage= 0;
                var timer = window.setInterval(()=>{
                    this.percentage += 5;
                    if (this.percentage > 95) {
                        this.percentage = 95;
                    }
                },2000);
                var loading = this.$loading({fullscreen:false,target:document.querySelector(".show_video")});
                console.log("视频提交中。。。")
                var formData = new FormData();
                formData.append('video', file);
                $.ajax({
                    url: this.api+"/api/v1/video/get_video_inspection/",
                    timeout:3600000,
                    type: "post",
                    data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                    cache: false,
                    contentType: false,
                    processData: false,
                    success:(response)=>{
                        this.percentage = 100;
                        window.clearInterval(timer);
                        loading.close();
                        console.log(response);
                        this.sexInfo= 5;
                        this.forceInfo= 5;
                        this.imageUrl= [];
                        this.markerInfo= [];
//                        this.uploadInfo(response);
//                        this.videoUrl={url:response.data.video_url} ;
//                        this.videoUrl={url:response.data.video};
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
                            this.first = false;
                        }else {
                            this.resetMarker(this.markerInfo);
                        }
                        this.isLoading = false;
                        this.$parent.changeUploadState(false);
                        console.log( this.imageUrl,this.markerTime);
                        console.log( response);
                        console.log( this.markerInfo);
                    },
					error:err=>{
                        loading.close();
                        console.log(err);
                        this.percentage = 0;
                        this.sexInfo = 201;
                        this.forceInfo = 201;
                        window.clearInterval(timer);
                        this.isLoading = false;
                        this.showMessage('上传失败,重新上传！');
                        this.$parent.changeUploadState(false);
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
            resetMarker(marker){
                this.player = videojs('video');
                var player = this.player;
                player.markers.reset(marker)
            },
            initVideo(item){
                this.player = videojs('video');
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
                            return marker.text;
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
                /****** 返回插件中当前标记的数组，按升序时间排序 ******/
                var getMarkers = player.markers.getMarkers()

                /****** 从视频中的当前时间转到下一个标记。 如果没有下一个标记，那么什么都不做 ******/

                $("#btn-next").click(function(){
                    player.markers.next();
                })

                /****** 从视频中的当前时间转到上一个标记。 如果没有上一个标记，那么什么都不做 ******/

                $("#btn-prev").click(function(){
                    player.markers.prev();
                })

                /****** 允许动态修改标记时间（传入原始标记对象） ******/
                $("#btn-confirm").click(function(){
                    var markers = player.markers.getMarkers();
                    var add_time = parseInt( $("#add-time").val() );
                    console.log(add_time);
                    for (var i = 0; i < markers.length; i++) {
                        markers[i].time += add_time;
                    }
                    //调用updateTime以立即反应UI中的更改
                    player.markers.updateTime();
                })

                /****** 删除给定索引数组中的标记（从0开始） ******/
                $("#btn-del").click(function(){
                    //player.markers.remove([1,3]);

                    //删除所有标记
                    player.markers.removeAll();
                })

                /****** 动态添加新标记 ******/
                $("#btn-add").click(function(){
                    player.markers.add([{
                        time: 40,
                        text: "I'm added dynamically"
                    }]);
                })

                /****** 重置视频中的所有标记（相当于removeAll后再设置） ******/
                $("#btn-reset").click(function(){
                    player.markers.reset([{
                        time: 4,
                        text: "I'm new"
                    },
                        {
                            time:2,
                            text: "I'm new too"
                        }]);
                })

                /*验证描点*/
                $('label.click').removeAttr('for').on('click', function() {
                    $('.box').scrollTop(200); //'xxx'表示滚动数值
                });
            },
		}
	}
</script>

<style scoped>
	/*视频样式begin*/
	.videoCheck{width: 1200px;margin: 0 auto;}
	.show_video_outer{height: 400px;width: 700px;}
	.show_video{height:440px;position: relative;overflow: hidden;}

	.show_video #video{width: 100%;height: 440px;}
	.video_result_outer{ width:350px; height: 440px;z-index: 99;background-color: white;box-shadow:5px 0 20px #c5cff1;margin-left: 20px;}
	.video_result_outer .result_title{font-size: 24px;color: #000000;text-align: center;height: 100px;padding-top: 30px;}
	.video_result_outer .result_title:before{content: "";background: url("../../assets/image/result_top_image.png") no-repeat center center;height: 23px;display: block;margin-bottom: 10px;}
	.video_image_outer{border: 1px solid #e2ecfc;min-height: 200px;margin-top: 20px;padding-left: 20px;width: 1050px;}
	.video_image_outer:first-child{color: #010101;font-size: 16px;line-height: 50px;}
	.evidence_info{height: 80px;line-height: 80px;font-size: 16px;}
	.video_image_item{height: 160px;width: 190px;padding-right: 20px;margin-bottom: 20px;position: relative;}
	.video_image_con .video_image_item img{height: 130px;width: 100%;display: block;object-fit: cover;}
	.video_image_con .video_image_item p{height: 30px;line-height:30px;font-size: 14px;text-align: center;border: 1px solid #e2ecfc;border-top: none;}
	.show_result_title{position: absolute;height: 20px;font-size: 0;line-height: 0}
	.show_result_title span{;font-size: 14px;line-height: 20px;display: inline-block;vertical-align: top;}
	.show_result_title span:nth-of-type(2){background-color: white;padding: 0 5px;}
	.show_result_title span:nth-of-type(1){line-height: 22px;padding: 0 10px;}
	.video_result_red_number{color: #ff524a;border: 1px solid #ff524a;}
	.video_result_red_title{background-color: #ff524a;color: white;}
	.video_result_orange_number{color: #ffac09;border: 1px solid #ffac09;}
	.video_result_orange_title{background-color: #ffac09;color: white;}
	.choose_again{color: #333333;font-size: 16px;height: 42px;width: 120px;line-height: 42px;margin: 40px auto;border: 1px solid #e1e3e7;text-align: center;cursor: pointer;}
	.inputfile{z-index: -11111;width: 0px;height:1px;opacity: 0;}
	.local_upload_video{height: 45px;line-height: 45px;font-size: 16px;margin: 40px auto;text-align: center;}
	.local_upload_video label{display:inline-block;color: #ffffff;font-size: 16px;height: 42px;width: 120px;line-height: 42px;border: 1px solid #e1e3e7;text-align: center;background-color: #316dff;cursor: pointer;}
	.local_upload_video p{display:inline-block;color: #666666;font-size: 16px;height: 42px;width: 120px;line-height: 42px;border: 1px solid #e1e3e7;text-align: center;background-color: #dddddd;cursor: pointer;}


	.show_json_outer .result_title{font-size: 24px;color: #000000;text-align: center;height: 100px;padding-top: 30px;}
	.show_json_outer .result_title:before{content: "";background: url("../../assets/image/result_top_image.png") no-repeat center center;height: 23px;display: block;margin-bottom: 10px;}
	.suggest{color: #b2b2b2;font-size: 14px;min-height: 30px;margin:8px 0;}

	.result_outer{margin: 20px auto;display: flex;color: #000000;height: 28px;line-height: 28px;width: 210px;}
	.result_outer p:nth-of-type(1){font-size: 16px;width: 90px;}
	.result_outer p:nth-of-type(2){font-size: 16px;width: 120px;text-align: center}
	.result_outer p:nth-of-type(3){font-size: 16px;flex: 4;text-align: center}
	.result_outer .green_style_name{background-color: #54cd62;border: 1px solid #54cd62;color: #fff}
	.result_outer .orange_style_name{background-color: #ffac09;border: 1px solid #ffac09;color: #fff}
	.result_outer .red_style_name{background-color: #ff524a;border: 1px solid #ff524a;color: #fff}


</style>