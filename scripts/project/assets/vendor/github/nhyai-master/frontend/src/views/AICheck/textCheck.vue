<template>
	<div class="textCheck">
		<!--音频评审-->
		<div class="clearfix content_style">
			<div class="show_voice_outer fl">
				<div class="outer_text">
					<p class="voice_title">文本审查</p>
					<div class="voice_result_outer">
						<div class="show_text_word">
							<!--<span class="fl"> 1:05 - 1:06</span>-->
							<!--<span class="fl ell"> 好，现在<span class="red_color">违禁词</span>到室当中呢，<span class="red_color">违禁词</span>了三十位</span>-->
						</div>
					</div>
				</div>
				<p class="suggest"><span class="red_color">*</span> 提示: 敏感系数<50%为合规，50%～80%为疑似违规，>80%为违规</p>
			</div>
			<div class="show_json_outer fl">
				<p class="result_title">审查结果</p>
				<!--<div class="result_outer" v-for="item in resultType">
					<p>{{item.firstType}}</p>
					<p class="red_style_name">违规</p>
				</div>
				<div class="result_outer" v-if="isUploadText">
					<p></p>
					<p class="green_style_name">识别中...</p>
				</div>-->
				<div>
					<div class="result_outer">
						<p>色情文字检测</p>
						<p class="green_style_name" v-if="isUploadText">识别中...</p>
						<p class="red_style_name" v-else-if="isSex">违规</p>
						<p class="green_style_name" v-else>合规</p>
					</div>
					<div class="result_outer">
						<p>涉政文字检测 </p>
						<p class="green_style_name" v-if="isUploadText">识别中...</p>
						<p class="red_style_name" v-else-if="isPolitics">违规</p>
						<p class="green_style_name" v-else>合规</p>
					</div>
					<div class="result_outer">
						<p>违禁品检测</p>
						<p class="green_style_name" v-if="isUploadText">识别中...</p>
						<p class="red_style_name" v-else-if="isForce">违规</p>
						<p class="green_style_name" v-else>合规</p>
					</div>
					<div class="result_outer">
						<p>民谣类检测</p>
						<p class="green_style_name" v-if="isUploadText">识别中...</p>
						<p class="red_style_name" v-else-if="isSong">违规</p>
						<p class="green_style_name" v-else>合规</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
    export default {
	    props:['stopAudio'],
	    data(){
            return{
				resultType:[],
                isUploadText:false,
                isError:false,
				isSex:false,
				isForce:false,
				isSong:false,
				isPolitics:false
			}
        },
		mounted(){
		},
		watch:{

		},
		methods:{

            submitText(e,file){
                console.log(file);
                document.getElementsByClassName('show_text_word')[0].innerHTML='';
                this.isUploadText = true;
                this.isSex = false;
                this.isPolitics = false;
                this.isSong = false;
                this.isForce = false;
                this.audioName = file.name;
                var loading = this.$loading({fullscreen:false,target:document.querySelector(".outer_text")});
                console.log("文本提交中。。。")
                var formData = new FormData();
                formData.append('text', file);
                $.ajax({
                    url: this.api+"/api/v1/text/get_text_recognition_inspection/",
                    type: "post",
                    data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                    cache: false,
                    contentType: false,
                    processData: false,
                    success:(response)=>{
                        console.log(response);
                        window.setTimeout(()=>{
                            console.log(document.getElementsByClassName('show_text_word')[0]);
                            document.getElementsByClassName('show_text_word')[0].innerHTML= response.data.web_text;
                            loading.close();
                            this.isUploadText = false;
                            this.$parent.changeUploadState(false);
                        },1000);
                        if(response.data.final_list.length!=0){
                            response.data.final_list.forEach(item=>{
                                if(item.indexOf('色情')!=-1){
									this.isSex = true;
								}else if(item.indexOf('政治')!=-1){
                                    this.isPolitics = true;
                                }else if(item.indexOf('民谣')!=-1){
                                    this.isSong = true;
                                }else if(item.indexOf('违禁品')!=-1){
                                    this.isForce = true;
								}
							});
						}
//                        if(response.data.sensitive_list.length!=0){
//                            this.resultType = response.data.sensitive_list;
//                            this.isNone = false;
//                            this.$parent.changeUploadState(false);
//                        }else {
//                            this.resultType=[];
//                            this.isNone = true;
//                            this.$parent.changeUploadState(false);
//                            loading.close();
//                        }
                    },
                    error:err=>{
                        loading.close();
                        console.log(err);
                        this.$message.error('上传失败,重新上传！');
                        this.$parent.changeUploadState(false);
                        this.isUploadText = false;
                        this.isError = true;
                    }
                });
                e.preventDefault();
            }
		}
	}
</script>

<style scoped>
	@import "../../assets/css/audio.css";
	/*音频样式begin*/
	.show_voice_outer{min-height: 440px;width: 800px;}
	.content_style{width: 1200px;margin: 0 auto;}
	.outer_text{height:500px;z-index: 1;text-align: center;background-color: #f4f5f7;padding-right: 20px;}
	.voice_title{height: 34px;line-height:34px;width: 135px;margin: 0 auto;background-color: #deecf9;color: #007bff;margin-bottom: 20px;}
	.voice_player_outer{height: 125px;width: 94%;margin: 10px auto;border-radius: 5px;background-color: white;}
	.voice_result_outer{height: 430px;background-color: white;width: 94%;margin: 10px auto;border-radius: 5px;overflow-y: scroll;overflow-x: hidden;}
	.audio_wrapper_outer{margin-left: 180px;margin-right: 20%;}
	.icon_music{margin: 25px 0 0 95px;}
	.show_text_word{margin: 20px ;color: #333;font-size: 14px;text-align: left;}
	/*.show_voice_word span{display: inline-block;text-align: left;}
	.show_voice_word span:nth-of-type(2){margin-left: 20px;flex: 1;}*/

	.show_json_outer{height: 430px;width:400px;z-index: 99;background-color: white;position: relative;left: -20px;top: 35px;box-shadow:5px 0 20px #c5cff1;overflow-y: scroll;}
	.show_json_outer .result_title{font-size: 24px;color: #000000;text-align: center;height: 100px;padding-top: 30px;}
	.show_json_outer .result_title:before{content: "";background: url("../../assets/image/result_top_image.png") no-repeat center center;height: 23px;display: block;margin-bottom: 10px;}
	.suggest{color: #b2b2b2;font-size: 14px;min-height: 30px;margin:8px 0;}
	.result_outer{margin: 20px auto;display: flex;color: #000000;height: 28px;line-height: 28px;width: 240px;}
	.result_outer p:nth-of-type(1){font-size: 16px;width: 120px;}
	.result_outer p:nth-of-type(2){font-size: 16px;width: 120px;text-align: center}
	.result_outer p:nth-of-type(3){font-size: 16px;flex: 4;text-align: center}
	.result_outer .green_style_name{background-color: #54cd62;border: 1px solid #54cd62;color: #fff;text-align: center;}
	.result_outer .green_style_number{border: 1px solid #54cd62;color: #54cd62}
	.result_outer .orange_style_name{background-color: #ffac09;border: 1px solid #ffac09;color: #fff}
	.result_outer .orange_style_number{border: 1px solid #ffac09;color: #ffac09}
	.result_outer .red_style_name{background-color: #ff524a;border: 1px solid #ff524a;color: #fff}
	.result_outer .red_style_number{border: 1px solid #ff524a;color: #ff524a}
	.orange_color{color: #ffac09;}
	.red_color{color: #ff524a;}
</style>