<template>
	<tr>
		<template v-if="!editing">
			<td>{{string.string}}</td>
			<td class="edit"><b-icon icon="pencil-alt" @click.native="editing=true; editString=string.string"></b-icon><b-icon icon="trash" @click.native="$emit('delete')"></b-icon></td>
		</template>
		<td v-else colspan="2">
			<b-field>
				<b-input placeholder="String" v-model="editString"
						 size="is-small">
				</b-input>
			</b-field>
			<b-taglist>
				<b-tag v-for="(sub, i) in predicted" :key="i" type="is-primary" @click.native="stringAdd(sub)">{{sub}}</b-tag>
			</b-taglist>
			<b-button class="edit-string" @click="editing=false">Cancel</b-button>
			<b-button class="edit-string" @click="doneString()">Done</b-button>
		</td>
	</tr>
</template>

<script>
	export default {
		name: "TargetString",
		props: ['string', 'predicted'],
		data() {
			return {
				editing: false,
				editString: ""
			}
		},
		methods: {
			stringAdd(sub) {
				if ((this.editString != "") & (this.editString[-1] != " ")) {
					this.editString += " ";
				}
				this.editString += sub.toLowerCase();
			},
			doneString() {
				this.editing = false
				this.string.string = this.editString
			}
		}
	};
</script>

<style scoped>

	.edit .icon {
		margin-left: 10px;
		float: right;
	}

	.button.edit-string {
		width: 50%;
	}

</style>
