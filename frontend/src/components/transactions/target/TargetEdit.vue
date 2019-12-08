<template>
	<div class="modal-card" style="width: auto">
		<header class="modal-card-head">
			<p class="modal-card-title">{{(target.id) ? 'Edit': 'New'}} Target</p>
		</header>
		<section class="modal-card-body">
			<b-field>
				<b-input placeholder="Target name" v-model="target.name"
						 size="is-large">
				</b-input>
			</b-field>
			<b-taglist>
				<b-tag v-for="(sub, i) in predicted_words" :key="i" type="is-primary" @click.native="nameAdd(sub)">{{sub}}</b-tag>
			</b-taglist>
			<div class="b-table strings">
				<table class="table">
					<thead>
					<tr>
						<th colspan="2">Strings</th>
					</tr>
					</thead>
					<tbody>
					<target-string v-for="string in target.strings"
								   :string="string"
								   :predicted="predicted_words"
								   :key="string.string"
								   @edit="string.string = $event"
								   @delete="delString(string)"></target-string>
					<tr>
						<td colspan="2" class="add">
							<b-button size="is-medium"
									  icon-left="plus-circle"
									  v-if="!addingString"
									  @click="addString()">
							Add String
							</b-button>
							<template v-else>
								<b-field>
									<b-input placeholder="String" v-model="newString"
											 size="is-small">
									</b-input>
								</b-field>
								<b-taglist>
									<b-tag v-for="(sub, i) in predicted_words" :key="i" type="is-primary" @click.native="stringAdd(sub)">{{sub}}</b-tag>
								</b-taglist>
								<b-button class="edit-string" @click="cancelString()">Cancel</b-button>
								<b-button class="edit-string" @click="doneString()">Add</b-button>
							</template>
						</td>
					</tr>
					</tbody>
				</table>
				<b-button v-if="target.id !== null" type="is-danger" @click="unlink()" icon-pack="fas" icon-left="unlink">Unlink</b-button>
				<b-button v-if="target.id !== null" type="is-danger" @click="delTarget()" icon-pack="fas" icon-left="trash">Delete Target</b-button>
			</div>
		</section>
		<footer class="modal-card-foot">
			<b-button type="button" @click="$parent.close()">Cancel</b-button>
			<b-button type="is-primary" @click="doneString(); $emit('save', target)" :loading="saving">Save</b-button>
		</footer>
	</div>
</template>

<script>
	import * as requests from "@/helpers/requests"
	import BButton from "buefy/src/components/button/Button";
	import TargetString from "@/components/transactions/target/TargetString";

	export default {
		name: "TargetEdit",
		components: { TargetString, BButton },
		props: ["transaction", "saving"],
		data() {
			let tgt = {
				id: null,
				name: '',
				internal: false,
				strings: []
			}
			if (this.transaction.target){
				tgt = JSON.parse(JSON.stringify(this.transaction.target))
			}
			return {
				target: tgt,
				addingString: false,
				newString: ""
			}
		},
		computed: {
			predicted_words(){
				let space_split = this.transaction.raw.split(' ')
				let split = []
				space_split.forEach(value => {
					split.push(...value.split(',').filter(value => {return value !== ""}))
				})
				return split
			}
		},
		methods: {
			fetchTarget(){
				requests.get(`target/${this.target.id}`).then(data => {
					this.target = data
				})
			},
			nameAdd(sub) {
				if ((this.target.name != "") & (this.target.name[-1] != " ")) {
					this.target.name += " ";
				}
				this.target.name += sub.charAt(0).toUpperCase() + sub.slice(1).toLowerCase();
			},
			stringAdd(sub) {
				if ((this.newString != "") & (this.newString[-1] != " ")) {
					this.newString += " ";
				}
				this.newString += sub.toLowerCase();
			},
			addString() {
				this.addingString = true;
				this.newString = "";
			},
			doneString() {
				if (this.newString.length > 0 && this.addingString){
					this.target.strings.push({string: this.newString, id: -1})
					this.addingString = false
				}
			},
			cancelString() {
				this.addingString = false
			},
			delString(string){
				this.target.strings = this.target.strings.filter(item => {
					return item !== string
				})
			},
			unlink(){
				this.$emit('unlink')
			},
			delTarget(){
				this.$dialog.confirm({
					message: `This target is associated with ${this.target.usages} transactions. Continue deleting?`,
					onConfirm: () => this.$emit('delete_target')
				})
			}
		},
		created() {
			if (this.transaction.id !== -1){
				this.fetchTarget()
			}
		}
	};
</script>

<style scoped>

	.modal-card-body {
		min-width: 50vw;
		min-height: 20vh;
		overflow: visible;
	}

	.strings {
		width: 100%;
	}

	.add .button {
		width: 100%;
	}

	.add .tags {
		margin-bottom: 0;
	}

	.add .button.edit-string {
		width: 50%;
	}

	.table thead th {
		color: black;
		text-align: center;
	}

	/deep/ .tag {
		cursor: pointer;
	}

	/deep/ .button {
		margin-top: 5px;
		width: 100%;
	}

</style>
