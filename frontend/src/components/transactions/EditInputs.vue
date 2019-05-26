<template>
	<div>
		<mdc-textfield v-model="value.name" @input="update" label="Name" class="name_in" />

		<mdc-chip-set v-if="predicted != ''">
			<mdc-chip v-for="(sub, index) in predicted_words" :key="index" @click="nameAdd(sub)" style="font-size: 0.6rem;">{{ sub }}</mdc-chip>
		</mdc-chip-set>

		<table style="width: 100%; font-family: Roboto; margin-top: 10px">
			<tr>
				<th style="font-size: 24px; padding: 5px;" colspan="2">Strings</th>
			</tr>
			<tr v-for="(s, index) in value.strings">
				<td v-if="!editStringDialog" style="text-align: left;">{{ s.string }}</td>
				<td v-if="!editStringDialog" style="text-align: center; width: 10%;">
					<mdc-icon icon="delete" @click.native="removeString(index)"></mdc-icon>
					<mdc-icon
						@click.native="
							editStringDialog = true;
							addStringDialog = false;
							tStringId = s.id;
							tString = s.string;
						"
						icon="edit"
					></mdc-icon>
				</td>
				<td v-else colspan="2">
					<mdc-textfield fullwidth v-model="tString" label="String" class="string_in"></mdc-textfield>
					<mdc-chip-set v-if="predicted != ''">
						<mdc-chip v-for="(sub, index) in predicted_words" :key="index" @click="stringAdd(sub)" style="font-size: 0.6rem;">{{ sub }}</mdc-chip>
					</mdc-chip-set>
					<mdc-button @click="editString">Add</mdc-button>
					<mdc-button @click="editStringDialog = false">Cancel</mdc-button>
				</td>
			</tr>
			<tr>
				<td v-if="!addStringDialog" style="text-align: center;" colspan="2">
					<span
						@click="
							addStringDialog = true;
							editStringDialog = false;
							tStringId = -1;
							tString = '';
						"
						><mdc-icon icon="add_circle" style="line-height: 34px; cursor: pointer"></mdc-icon
					></span>
				</td>
				<td v-else>
					<mdc-textfield fullwidth v-model="tString" label="String" class="string_in"></mdc-textfield>
					<mdc-chip-set v-if="predicted != ''">
						<mdc-chip v-for="(sub, index) in predicted_words" :key="index" @click="stringAdd(sub)" style="font-size: 0.6rem;">{{ sub }}</mdc-chip>
					</mdc-chip-set>
					<mdc-button @click="editString">Add</mdc-button>
					<mdc-button @click="addStringDialog = false">Cancel</mdc-button>
				</td>
			</tr>
		</table>
	</div>
</template>

<script>
export default {
	name: "EditInputs",
	props: ["value", "predicted"],
	data() {
		return {
			tString: "",
			tStringId: -1,
			//name: this.value.name,
			//strings: this.value.strings,
			editStringDialog: false,
			addStringDialog: false
		};
	},
	computed: {
		predicted_words(){
			let space_split = this.predicted.split(' ')
			let split = []
			space_split.forEach(value => {
				split.push(...value.split(',').filter(value => {return value !== ""}))
			})
			return split
		}
	},
	methods: {
		update() {
			this.$emit("input", { name: this.value.name, strings: this.value.strings });
		},
		nameAdd(sub) {
			if ((this.value.name != "") & (this.value.name[-1] != " ")) {
				this.value.name += " ";
			}
			this.value.name += sub.charAt(0).toUpperCase() + sub.slice(1).toLowerCase();
			this.update();
		},
		stringAdd(sub) {
			if ((this.tString != "") & (this.tString[-1] != " ")) {
				this.tString += " ";
			}
			this.tString += sub.toLowerCase();
		},
		removeString(index) {
			this.value.strings.splice(index, 1);
		},
		editString() {
			this.value.strings.push({ id: this.tStringId, string: this.tString });
			this.update();
			this.editStringDialog = false;
			this.addStringDialog = false;
		}
	}
};
</script>

<style>
.name_in .mdc-floating-label {
	font-size: 2rem;
	line-height: 1.4rem;
	color: #ffffff !important;
}

.mdc-text-field:not(.mdc-text-field--disabled):not(.mdc-text-field--outlined):not(.mdc-text-field--textarea) .mdc-text-field__input,
.mdc-text-field:not(.mdc-text-field--disabled):not(.mdc-text-field--textarea){
	border-bottom-color: rgba(255, 255, 255, 0.42) !important;
}

.name_in .mdc-floating-label--float-above {
	-webkit-transform: translateY(-100%) scale(0.5);
	transform: translateY(-100%) scale(0.5);
	color: #007d51 !important;
}

.name_in input {
	font-size: 2rem;
	color: #ffffff !important;
}


.string_in input {
	color: #ffffff !important
}
	.string_in input::placeholder {
		color: #ffffff !important
	}
</style>

<style scoped>
.name_in {
	width: 100%;
}

table,
th,
td {
	border: 1px solid rgba(255, 255, 255, 0.42);
	border-collapse: collapse;
}
</style>
