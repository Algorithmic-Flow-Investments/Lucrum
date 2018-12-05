<template>
<div>
	<mdc-dialog v-model="stringDialog"
				title="Add String" @accept="editString()"
				@cancel="" accept="Add" cancel="Cancel">
		<mdc-textfield fullwidth v-model="tString" label="String" class="string_in"></mdc-textfield>
		<mdc-chip-set v-if="predicted != ''">
			<mdc-chip v-for="(sub, index) in predicted.split(' ')" :key="index" @click="stringAdd(sub)" style="font-size: 0.6rem;">{{sub}}</mdc-chip>
		</mdc-chip-set>
	</mdc-dialog>

	<mdc-textfield v-model="value.name" @input="update" label="Name" class="name_in"/>

	<mdc-chip-set style="width: 90%; margin-left: 5%;" v-if="predicted != ''">
		<mdc-chip v-for="(sub, index) in predicted.split(' ')" :key="index" @click="nameAdd(sub)" style="font-size: 0.6rem;">{{sub}}</mdc-chip>
	</mdc-chip-set>

	<table style="width: 90%; margin-left: 5%; font-family: Roboto; margin-top: 10px">
		<tr>
			<th style="font-size: 24px" colspan="2">Strings</th>
		</tr>
		<tr v-for="(s, index) in value.strings">
			<td style="text-align: left;">{{s.string}}</td>
			<td style="text-align: right; width: 15%;"><mdc-icon icon="delete" @click.native="removeString(index)" style="color: rgb(55, 55, 64)"></mdc-icon> <mdc-icon @click.native="stringDialog=true; tStringId=s.id; tString=s.string" icon="edit" style="color: rgb(55, 55, 64)"></mdc-icon></td>
		</tr>
		<tr>
			<td style="text-align: center;" colspan="2">
				<span @click="stringDialog=true; tStringId=-1; tString=''"><mdc-icon icon="add_circle" style="color: rgb(55, 55, 64)"></mdc-icon></span>
			</td>
		</tr>
	</table>
</div>
</template>

<script>
  export default {
	name: 'EditInputs',
	props: ['value', 'predicted'],
	data () {
	  return {
		tString: '',
		tStringId: -1,
		//name: this.value.name,
		//strings: this.value.strings,
		stringDialog: false,
	  }
	},
	methods: {
	  update() {
		this.$emit('input', {name: this.value.name, strings: this.value.strings})
	  },
	  nameAdd(sub){
		if (this.value.name != '' & this.value.name[-1] != ' '){
		  this.value.name += ' '
		}
		this.value.name += sub.charAt(0).toUpperCase() + sub.slice(1).toLowerCase()
		this.update()
	  },
	  stringAdd(sub){
		if (this.tString != '' & this.tString[-1] != ' '){
		  this.tString += ' '
		}
		this.tString += sub.toLowerCase()
	  },
	  removeString(index){
	    this.value.strings.splice(index, 1)
	  },
	  editString(){
		this.value.strings.push({id:this.tStringId, string:this.tString})
		this.update()
	  },
	}
  }
</script>

<style>
	.name_in .mdc-floating-label {
		font-size: 2rem;
		line-height: 1.4rem;
	}

	.name_in .mdc-floating-label--float-above {
		-webkit-transform: translateY(-100%) scale(0.50);
		transform: translateY(-100%) scale(0.50);
		color: #007d51 !important;
	}

	.name_in .mdc-text-field__input {
		font-size: 2rem;
	}

	.mdc-dialog__body {
		margin-top: 0;
	}

	.fullpage .mdc-dialog__header__title {
		color: #1eb980
	}
</style>

<style scoped>

	.name_in {
		width: 90%;
		margin-left: 5%;
		margin-top: 20%;
	}




	table, th, td {
		border: 1px solid black;
		border-collapse: collapse;
	}

</style>
