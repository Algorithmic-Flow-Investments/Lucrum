import * as requests from "@/helpers/requests";

export default class Account {
	constructor(data) {
		this.unpack(data);
	}

	unpack(data) {
		this.id = data.id;
		this.name = data.name || "";
		this.balance = data.balance || 0;
		this.description = data.description || "";
		this.usages = data.usages || [];
		this.balance_graph = data.balance_graph || {};
		this.calculated_balance = data.calculated_balance || this.balance;
	}

	fetch() {
		if (!this.id) return;
		requests.get(`accounts/get/${this.id}`).then(data => {
			this.unpack(data)
		})
	}
}
