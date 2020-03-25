import moment from "moment";
import Target from "@/Models/Target";
import Method from "@/Models/Method";
import Account from "@/Models/Account";
import * as requests from "@/helpers/requests";
import store from "@/store";


export default class Transaction {
	constructor(data) {
		this.unpack(data);
	}

	unpack(data) {
		this.id = data.id || this.id;
		this.amount = data.amount || this.amount || 0;
		this.date = moment(data.date) || this.date || moment();
		this.account_id = data.account_id || this.account_id || null;
		this.account = this.getAccount()
		this.target_id = this.target_id || null;
		if (data.target_id !== undefined) {
			this.target_id = data.target_id
		}
		this.target = this.getTarget()
		this.method_id = this.method_id || null;
		if (data.method_id !== undefined) {
			this.method_id = data.method_id
		}
		this.method = this.getMethod()
		this.tag_ids = this.tag_ids || [];
		if (data.tag_ids !== undefined) {
			this.tag_ids = data.tag_ids
		}
		this.tags = this.getTags()
		this.raw_info = data.raw_info || this.raw_info || "";

		this.extra = this.extra || {}

		this.extra.date = data.date_extra || {}
	}

	fetch() {
		if (!this.id) return;
		requests.get(`transactions/get/${this.id}`).then(data => {
			this.unpack(data)
		})
	}

	unlinkTarget() {
		this.target_id = null
		this.target = this.getTarget()
	}

	commit() {
		return new Promise((resolve, reject) => {
			if (this.id) {
				requests.post(`transactions/update/${this.id}`, this).then(data => {
					this.unpack(data)
					resolve()
				}).catch(exception => reject(exception))
			} else {
				requests.post(`transactions/add`, this).then(() => resolve()).catch(exception => reject(exception))
			}
		})
	}

	toJSON() {
		return {
			id: this.id,
			amount: this.amount,
			date: this.date.format("YYYY-M-D"),
			target_id: this.target_id,
			method_id: this.method_id,
			account_id: this.account_id,
			tag_ids: this.tag_ids,
			raw_info: this.raw_info,
		}
	}

	getTarget() {
		let data = store.state.targets
		if (this.target_id === null) {
			return null
		}
		return data.filter(t => t.id === this.target_id)[0]
	}

	getMethod() {
		let data = store.state.methods
		if (this.method_id === null) {
			return null
		}
		return data.filter(t => t.id === this.method_id)[0]
	}

	getAccount() {
		let data = store.state.accounts
		return data.filter(t => t.id === this.account_id)[0]
	}

	getTags() {
		let data = store.state.tags
		return data.filter(t => this.tag_ids.includes(t.id))
	}
}
