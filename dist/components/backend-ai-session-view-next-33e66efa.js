import{_ as s,e as i,B as t,c as a,I as r,a as e,i as o,x as n,j as m,k as c}from"./backend-ai-webui-56a57161.js";import"./backend-ai-session-launcher-91dbf2eb.js";import"./backend-ai-session-view-49a5958c.js";import"./lablup-codemirror-cfaa7005.js";import"./lablup-progress-bar-29666bb5.js";import"./slider-6076538b.js";import"./mwc-check-list-item-b24ec567.js";import"./media-query-controller-d2b7b94d.js";import"./dir-utils-fec807e6.js";import"./vaadin-grid-5b4c4952.js";import"./vaadin-grid-filter-column-e0749f8b.js";import"./vaadin-grid-selection-column-d7c5ba92.js";import"./json_to_csv-35c9e191.js";import"./backend-ai-resource-monitor-edce2ea6.js";import"./mwc-switch-be8a973a.js";import"./backend-ai-list-status-712186f5.js";import"./lablup-grid-sort-filter-column-9fca2927.js";import"./vaadin-grid-sort-column-d2fa540e.js";import"./vaadin-iconset-3cf18983.js";import"./lablup-activity-panel-375f75db.js";import"./mwc-formfield-f4b36fa9.js";import"./mwc-tab-bar-b177b3ef.js";let p=class extends t{static get styles(){return[a,r,e,o``]}async _viewStateChanged(s){await this.updateComplete}render(){return n`
      <backend-ai-react-session-list
        @moveTo="${s=>{const i=s.detail.path;globalThis.history.pushState({},"",i),m.dispatch(c(decodeURIComponent(i),{}))}}"
      ></backend-ai-react-session-list>
    `}};p=s([i("backend-ai-session-view-next")],p);
