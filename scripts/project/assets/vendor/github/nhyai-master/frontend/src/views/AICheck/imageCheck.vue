<template>
	<div class="imageCheck">
		<!--图片评审-->
		<!--<el-row style="min-width: 800px;margin-top: 30px">
			<el-col :md={span:14,offset:2} :lg={span:13,offset:2} :xl={span:11,offset:4}>-->
		<div style="width: 1200px;margin: 0 auto;"class="clearfix">
			<div class="show_add_image_outer fl" >
				<div class="outer_add">
					<div class="show_image_outer">
						<img class="show_add_image" :src="dialogImageUrl">
					</div>
					<div class="show_result_outer" >
						<div v-show="forceLevel!=200">
							<div class="show_result" v-if="isForce">
								<i class="show_word danger_result_back"></i>
							</div>
							<div class="show_result" v-else>
								<!--<i class="show_word normal_result_back"></i>-->
								<i class="show_word normal_result_back"></i>
							</div>
						</div>

					</div>
				</div>
				<p class="suggest"><span style="color: red">*</span> 提示: 敏感系数<50%为合规，50%～80%为疑似违规，>80%为违规<span v-show="imageIsBig" style="color: red;margin-left: 10px;display: inline-block;">！该图片大小超过1M</span></p>
			</div>
			<!--</el-col>-->
			<!--<el-col :md="6" :lg="7" :xl="5">-->
			<div class="show_json_outer fl">
				<p class="result_title">审查结果</p>
				<div class="result_outer">
					<p>暴恐识别</p>
					<p class="green_style_name" v-if="forceLevel==200">识别中...</p>
					<p class="red_style_name" v-else-if="forceLevel>90">违规</p>
					<p class="orange_style_name" v-else-if="forceLevel>50">疑似违规</p>
					<p class="green_style_name" v-else>合规</p>
					<p class="green_style_number" v-if="forceLevel==200"></p>
					<p class="red_style_number" v-else-if="forceLevel>90">{{forceLevel}}%</p>
					<p class="orange_style_number" v-else-if="forceLevel>50">{{forceLevel}}%</p>
					<p class="green_style_number" v-else>{{forceLevel}}%</p>
				</div>
				<div class="result_outer">
					<p>色情识别</p>
					<p class="green_style_name" v-if="sexLevel==200">识别中...</p>
					<p class="red_style_name" v-else-if="sexLevel>90">违规</p>
					<p class="orange_style_name" v-else-if="sexLevel>50">疑似违规</p>
					<p class="green_style_name" v-else>合规</p>
					<p class="green_style_number" v-if="sexLevel==200"></p>
					<p class="red_style_number" v-else-if="sexLevel>90">{{sexLevel}}%</p>
					<p class="orange_style_number" v-else-if="sexLevel>50">{{sexLevel}}%</p>
					<p class="green_style_number" v-else>{{sexLevel}}%</p>
				</div>
				<!--<div class="result_outer">
					<p class="ell">政治敏感识别</p>
					<p class="orange_style_name">疑似违规</p>
					<p class="orange_style_number">60.35%</p>
				</div>
				<div class="result_outer">
					<p>公众人物识别</p>
					<p class="red_style_name">违规</p>
					<p class="red_style_number">90.35%</p>
				</div>
				<div class="result_outer">
					<p>广告检测</p>
					<p class="red_style_name">违规</p>
					<p class="red_style_number">90.16%</p>
				</div>-->
			</div>
		</div>

			<!--</el-col>-->
		<!--</el-row>-->
	</div>
</template>

<script>
    import fileUtil from '../../store/fileUtil'
	export default {
        props:["file"],
	    data(){
	        return{
                dialogImageUrl: require("../../assets/image/sample_image.png"),
                isForce:false,
                imageRight:false,
                imageIsBig:false,
				sexLevel:'12.99',
                forceLevel:'5.74'

			}
		},
		methods:{
	      submitImage(e,file,url){
	          console.log(file);
	          this.sexLevel=200;
	          this.forceLevel=200;
              var loading;
              fileUtil.getOrientation(file).then((orient) => {
                  if(orient && orient === 6) {
                      const reader = new FileReader();
                      reader.onload = ($event)=> {
                          let img = new Image();
                          img.src = $event.target.result;
                          img.onload = ()=> {
                              const data = fileUtil.rotateImage(img, img.width, img.height);
                              const newFile = fileUtil.dataURLtoFile(data, file.name);
                              console.log(newFile);
                              this.dialogImageUrl= fileUtil.getObjectURL(newFile);
                              loading = this.$loading({fullscreen:false,target:document.querySelector(".show_result_outer")});
                          }
                      };
                      reader.readAsDataURL(file);
                  } else {
                      this.dialogImageUrl= fileUtil.getObjectURL(file);
                      loading = this.$loading({fullscreen:false,target:document.querySelector(".show_result_outer")});
                  }
                  console.log("图片提交中。。。");
                  var formData = new FormData();
                  formData.append('image', file);
                  $.ajax({
                      url: this.api+"/api/v1/image/get_image_inspection/",
                      type: "post",
                      data: formData,
//                    headers: {'Authorization': 'Token mytoken'},
                      cache: false,
                      contentType: false,
                      processData: false,
                      success:(response)=>{
                          loading.close();
                          console.log(response);
//                      this.dialogImageUrl = response.image;
                          this.sexLevel = response.data.porn_percent;
                          this.forceLevel = response.data.violence_percent;
                          if(this.sexLevel>50|this.forceLevel>50){
                              this.isForce = true;
                          }else {
                              this.isForce = false;
                          }
                          this.$parent.changeUploadState(false);
                      },
                      error:err=>{
                          loading.close();
                          console.log(err)
                          this.$parent.changeUploadState(false);
                      }
                  });
              });

              e.preventDefault();
		  }
		}
	}
</script>
<style scoped>
	/*image样式begin*/
	.current_width_style{width: 1200px;margin: 0 auto;}
	.show_add_image_outer{min-height: 400px;width: 800px;}
	.show_input_outer{display: flex;}
	.show_word{width: 180px;height: 200px;  display: inline-block;  text-align: center;  font-size: 22px;  font-style: normal;  color: #fff;  box-sizing: border-box;  padding-top: 58px;}
	.normal_result_back{background-image: url("../../assets/image/normal_image_sample.png");background-repeat: no-repeat;position: absolute;top: 50%;left: 50%;margin-left: -90px;margin-top: -100px;}
	.danger_result_back{background-image: url("../../assets/image/2.png");}
	.show_json_outer{height: 430px;width:400px;z-index: 99;background-color: white;position: relative;left: -20px;top: 35px;box-shadow:5px 0 20px #c5cff1}
	.show_json_outer .result_title{font-size: 24px;color: #000000;text-align: center;height: 100px;padding-top: 30px;}
	.show_json_outer .result_title:before{content: "";background: url("../../assets/image/result_top_image.png") no-repeat center center;height: 23px;display: block;margin-bottom: 10px;}
	.suggest{color: #b2b2b2;font-size: 14px;min-height: 30px;margin:8px 0;}
	.show_result_outer{width: 100%;height: 100%;position: absolute;top: 0;z-index: 1;text-align: center; background-color: rgba(0,0,0,.2);}
	.show_result_outer:before{content: '';position: absolute;left: 0;top: 0;width: 100%;height: 100%;}
	.show_result{ z-index: 3;display: inline-block;vertical-align: middle;margin-top: 15%}
	.result_outer{margin: 20px auto;display: flex;color: #000000;height: 28px;line-height: 28px;width: 280px;}
	.result_outer p:nth-of-type(1){font-size: 16px;flex: 2.5;}
	.result_outer p:nth-of-type(2){font-size: 16px;flex: 3;text-align: center}
	.result_outer p:nth-of-type(3){font-size: 16px;flex: 2;text-align: center}
	.result_outer .green_style_name{background-color: #54cd62;border: 1px solid #54cd62;color: #fff}
	.result_outer .green_style_number{border: 1px solid #54cd62;color: #54cd62}
	.result_outer .orange_style_name{background-color: #ffac09;border: 1px solid #ffac09;color: #fff}
	.result_outer .orange_style_number{border: 1px solid #ffac09;color: #ffac09}
	.result_outer .red_style_name{background-color: #ff524a;border: 1px solid #ff524a;color: #fff}
	.result_outer .red_style_number{border: 1px solid #ff524a;color: #ff524a}
	.show_image_outer{vertical-align: middle;display: table-cell;text-align: center;width: 800px;height: 500px;}
	.show_add_image{max-height: 500px;max-width: 800px;}
	.outer_add{height:500px;position: relative;overflow: hidden;}

	/*image样式end*/

</style>