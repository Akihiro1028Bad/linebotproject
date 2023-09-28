import os
from dotenv import load_dotenv


# 操作文字
const_text_return = "最初に戻る"
const_text_cansel = "キャンセル"

# 各操作　基本
const_default = "default"
const_operation_add = "予定の追加"
const_operation_confirmation = "予定の確認"
const_operation_edit = "予定の編集"
const_operation_erase = "予定の消去"
const_operation_remind = "リマインド"

# 追加フロー
const_begin_date_input_wait = "begin_date_input_wait"  # 終了日時入力待ち
const_finish_date_input_wait = "finish_date_input_wait"  # 終了日時入力待ち
const_title_input_wait = "title_input_wait"  # タイトル入力待ち
const_temp_confirmation_wait = "temp_confirmation_wait"  # 一時的に入力内容確認待ち
const_location_input_wait = "location_input_wait"  # 場所入力待ち
const_detail_input_wait = "detail_input_wait"  # 詳細情報入力待ち
const_confirmation_wait = "confirmation_wait"  # 入力内容確認待ち

# 予定の確認フロー
const_ask_date = "ask_date"

# クライアント情報
if os.environ.get('PRODUCTION') is None:
    load_dotenv()

    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
    LINE_SECRET = os.environ.get("LINE_SECRET")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    REDIRECT_URI = os.environ.get("REDIRECT_URI")
    INSTA_PROCESS_URL = os.environ.get("INSTA_PROCESS_URL")
    GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")

else:
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
    LINE_SECRET = os.environ.get("LINE_SECRET")
    DATABASE_URL = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://")  # 本番用です
    REDIRECT_URI = os.environ.get("REDIRECT_URI")
    INSTA_PROCESS_URL = os.environ.get("INSTA_PROCESS_URL")
    GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")


messages = [
    # 名言系
    "🌅 起きて行動すること。それが成功の最初の鍵だ。🔑 ヴィンセント・ヴァン・ゴッホの言葉を胸に、今日も一日頑張りましょう！💪✨",
    "🔄 人生の90%は、出来事にどう対応するかだと、チャールズ・R・スウィンドールは言いました。今日も🌟ポジティブに頑張りましょう！",
    "🚶‍♂️ ロバート・K・ヤマガタが言った通り、可能性を信じることが、成功への第一歩。今日もその一歩を踏み出しましょう！",
    "🌱 今日の努力が明日の成功を生み出します。ロバート・コリヤーの言葉を忘れず、一日を全力で生きましょう！",
    "🚀 アインシュタインも言っています、やり続けること。それが成功の秘訣。今日も絶えず前進しましょう！",
    "💡 挑戦することが、人生を面白くする。ジョシュア・J・マリンの言葉を胸に、新しい一日に挑戦しましょう！",
    "🌄 日本のことわざに「何事も最初は難しい」とありますが、その先には必ず成果が待っています。今日も一日頑張りましょう！",
    "💡 失敗は成功の母。トーマス・エジソンの言葉を思い出し、恐れずに今日も挑戦しましょう！",
    "🌟 マリリン・モンローが言う通り、自分を信じること。それが成功の秘訣。今日も自分を信じて頑張りましょう！",
    "🌈 シェリル・サンドバーグが教えてくれるように、難しいことをやる勇気があれば、人生はもっと簡単になります。今日も勇気を持って一日を過ごしましょう！",
    "🏞 「成功とは、失敗を恐れずに夢を追い続けることだ」と、ナポレオン・ヒルは言いました。恐れずに前進し、今日も一日頑張りましょう！",
    "📚 マハトマ・ガンジーは「生きることは学ぶこと」と言いました。今日も新しいことを学び、一歩一歩前進しましょう！"
    "⏳「あなたの時間は限られている。他人の人生を生きることで時間を無駄にしてはいけない」と、スティーブ・ジョブズは伝えました。🚀自分らしく、今日も一日頑張りましょう！",
    "🚧「困難は成功への道中で出会うもの、行き止まりではない」と、ランディ・パウシュは教えています。🌄困難を乗り越え、今日も一日頑張りましょう！",
    "💡トマス・エジソンは「失敗は成功のもと」と言いました。🔥どんな挑戦も経験として受け入れ、今日も一日頑張りましょう！",
    "👣「一歩を踏み出さなければ、常にその場所に留まることになる」と、モーゼス・マローンは言いました。🏞新しい一歩を踏み出し、今日も頑張りましょう！",
    "🌌「夢を持つことは、魂の翼を持つこと」と、カール・サンドバーグは言いました。🦋夢を大切にし、今日も一日頑張りましょう！",
    "🚶「最も大切なのは、止まらないことだ」とアルバート・アインシュタインは教えています。🏃‍♂️止まらずに進み続け、今日も一日頑張りましょう！",
    "🔄「成功は、継続的に努力を続けることで得られる」と、コリン・パウエルは言いました。💪努力を継続し、今日も頑張りましょう！",
    "❤️「自分の力を信じ、前進し続ける勇気を持て」と、ヘレン・ケラーは言いました。🌟信念を持ち、今日も一日頑張りましょう！",
    "👊「成功とは、繰り返しの失敗を経験すること、ただし失敗を放棄しないことだ。」- ウィンストン・チャーチル。🌈失敗を恐れず、今日も一歩を踏み出しましょう！",
    "🎯「人生で最も大切なのは、自分が何を求めているか知ることだ。」- オラクルのデルフォイ。🚀自分の目標に向かって、今日も力強く進みましょう！",
    "📖「人は経験によって賢くなるのではない。経験したことを考えることで賢くなる。」- ソクラテス。🤔今日の経験も、深く考えることで成長の糧としましょう！",
    "⏰「あなたが今日のためにできることを、明日のために遅らせるな。」- ベンジャミン・フランクリン。🎉今日が新しいチャンスです、活用しましょう！",
    "💪「勇気は、一度も失敗しないことではない。何度も失敗しても、くじけないことだ。」- テッド・ルーズベルト。🔥挫折を乗り越えて、前進しましょう！",
    "🌟「可能性を見るための最良の方法は実行することだ。」- アラン・ケイ。✨可能性を信じて、新しいことにチャレンジしましょう！",
    "❤️「人生の意味は、生きることに意味を持たせることだ。」- ヴィクトール・フランクル。🌱今日も自分らしい一日を過ごしましょう！",
    "🧘「最も長い旅は、内なる自分への旅だ。」- プラタナス。🌌内省の時を持ち、自分自身を深く理解しましょう。"
    "🔮「未来について考える最善の方法は、それを創ることだ。」- アラン・ケイ。🌱\n自分の未来は自分の手で切り開きましょう！🚀",
    "🌟「人は自分を信じれば、どんな困難も乗り越えられる。」- マハトマ・ガンジー。✨\n自分を信じて、進む力を持ちましょう！🏃",
    "🌌「人生は夢である。目覚めるときその美しさを失うのだ。」- ペドロ・カルデロン・デ・ラ・バルカ。🌠\n夢を追い続け、人生の美しさを楽しみましょう！🌈",
    "🤝「一緒に行動することは、進歩の開始だ。」- ヘンリー・フォード。🌐\n共に助け合い、今日も一日頑張りましょう！💪",
    "🧠「人は考える草食動物である。」- ヴォルテール。💭\n深く考え、今日も自分の意志で行動しましょう！🚀",
    "🔍「人生とは、自分を発見することだ。死とは、それを他人に示すことだ。」- ブルース・リー。🌟\n毎日、自分自身を磨き続けましょう！🌱",
    "⏳「一瞬の完全な注意は、長い間の無関心よりも価値がある。」- アンドレ・ギード。⌛\n今日も心をこめて、一つ一つのことに取り組みましょう！💡",
    "🥇「勝者は決して放棄しない。放棄者は決して勝たない。」- ヴィンス・ロンバルディ。🏆\n最後まで諦めずに、今日も挑戦しましょう！🔥",
    "📘「人生の喜びは、新しいことを始めることにある。」- フョードル・ドストエフスキー。📕\n新しいチャレンジに挑戦して、今日も一日を楽しみましょう！🎉",
    "⭐「夢を見ることをやめるな。時間は流れるが、人生は止まっている。」- フランクリン・D・ルーズベルト。🌌\n夢を大切にして、今日も前に進みましょう！🚀",
    "🚴「人生は自転車に乗ることと似ている。均衡を保つためには前に進む必要がある。」- アルベルト・アインシュタイン。🌍\nどんな困難も乗り越えて、進む勇気を持ちましょう！🔥",
    "🎨「人生の最も深い原則は、選択の自由である。」- パブロ・ピカソ。🔮\n今日も自分の選択を信じて、自分の道を歩みましょう！🚶",
    "⚖️「人生は70%のどうしようもないことと、30%の自分の努力でできている。」- ジャック・キャンフィールド。💪\nその30%を最大限に活かして、今日も努力しましょう！🔥",
    "🌄「失敗は避けられない。それは成功への一歩だ。」- マイケル・ジョーダン。🌅\n失敗を恐れずに、今日もチャレンジしましょう！💪",
    "🌍「人生は問題を解決する過程である。」- ソクラテス。🧩\n問題や困難は成長のチャンス。前向きに取り組みましょう！🌟",
    "🌟「人生は10% 何が起こるか、90% それにどう対処するかだ。」- チャールズ・R・スウィンドール。🌈\n今日の出来事にどう対処するか、その選択はあなた次第です！🔮",
    "🎨「成功するための最良の方法は、一度成功することだ。」- パブロ・ピカソ。🌟\n一度の成功が次へのステップ。今日も自分を信じて進みましょう！🚀",
    "🌄「行動の価値は、それを達成することにある。」- アンベール・カミュ。🌅\n考えるだけでなく、行動する勇気を持ちましょう！💪",
    "📚「知識は力である。」- フランシス・ベーコン。💡\n毎日少しずつでも学ぶことで、自分を強くできます！🌱",
    "🎙️「最も勇気のあることは、自分の考えを明確に思い、それを他人に声高に語ることだ。」- トーマス・ジェファーソン。🌟\n自分の考えを大切に、今日も一歩前に進みましょう！🚀",
    "🍃「変わることを恐れず、学び続けること。これが青春だ。」- アルベルト・アインシュタイン。🌱\n新しいことを学び、変わる勇気を持ちましょう！🌟",
    "🥇「成功とは、繰り返し失敗をすること、ただし失望しないことだ。」- ウィンストン・チャーチル。🏆\n失敗を恐れず、常に前向きに取り組みましょう！🔥",
    "🌟「自分自身を信じること。それが成功の秘訣だ。」- ヴォルテール。✨\n自分を信じ、今日も最善を尽くしましょう！🏃",
    "🌍「人生は挑戦すること。それが人生の真の喜びだ。」- リチャード・ブランソン。🧩\n新しい挑戦を恐れず、今日も楽しんで過ごしましょう！🎉",
    "🌄「過去は変えられない。未来は変えることができる。」- マザー・テレサ。🌅\n今日という日を大切に、未来に影響を与える行動をしましょう！💪",
    "🔍「小さなことを積み重ねることが、とてつもなく大きな結果を生む。」- マンディ・ヘイル。🌟\n日常の小さな努力が、大きな成果につながります！🌱",
    "🌄「七転び八起き」- 日本のことわざ。🌅\n何度つまずいても立ち上がる勇気を持ちましょう！💪",
    "⭐「人生における最大の冒険は、自分の夢を追い求めることだ。」- ワンピース。🌌\n夢を追い続ける勇気を持ちましょう！🚀",
    "🌄「一度きりの人生だ、後悔しないように生きるんだ。」- 3年A組。🌅\n今日も自分の選択を信じて進みましょう！💪",
    "🌠「夢見ることを怠らない。夢は現実の扉だ。」- パウル・コエーリョ。✨\n夢を大切に、今日も一歩一歩進みましょう！🚀",
    "🔍「人生で最も大切なのは、何を持っているかではなく、どう使うかだ。」- トーマス・エジソン。🌟\n持っているものを最大限に活用しましょう！🌱",
    "❤️「宝物には形がない。それが、心を形にしたものだ。」- 魔女の宅急便。💎\n心の宝物を大切に、今日も一日を過ごしましょう！🌈",
    "🌄「自分を信じること。それが人生のスタートラインだ。」- ナルト。🌅\n自分を信じて、今日も最善を尽くしましょう！💪",
    "🌍「時は流れるが、思い出は永遠に残る。」- 村上春樹。🌌\n今日の一瞬一瞬を大切に、美しい思い出を作りましょう！📸",
    "🌄「失敗は成功のもと。」- 日本のことわざ。🌅\n失敗を恐れず、チャレンジし続けましょう！💪",
    "❤️「人は人を愛することで、完全になる。」- 星の王子様。💞\n愛を持って、今日も人との関わりを大切にしましょう！🌈",
    "🌍「人は一人では生きられない。」- 進撃の巨人。🧩\n周りの人々とのつながりを大切に、今日も支え合いましょう！🤝",
    "🎭「人生は舞台のようなもの。どんな役でも全力で演じきるのだ。」- ウィリアム・シェイクスピア。🌟\n今日も自分の役を全力で演じましょう！🎬",
    "🌄「過去は変えられないが、未来は変えることができる。」- 龍が如く。🌅\n未来に向けて、今日も一歩を踏み出しましょう！💪",
    "🌠「夢を見ることは、星空を見上げることだ。」- オズの魔法使い。✨\n無限の可能性を信じて、今日も夢を追い続けましょう！🚀",
    "🌄「一歩を踏み出す勇気が、人生を変える。」- 映画「君の名は」。🌅\n新しいことに挑戦する勇気を持ちましょう！💪",
    "🌍「信じることが、成功への最初のステップだ。」- マハトマ・ガンジー。🧩\n自分の力を信じて、今日も一日を進めましょう！🌟",
    "🌄「人生には選択がある。受け入れるか変えるかだ。」- シン・エヴァンゲリオン。🌅\n自分の人生をコントロールする決意を持ちましょう！💪",
    "🌱「強さは、大きな力ではなく、継続する能力にある。」- アインシュタイン。🌟\nコツコツと努力を続けることで、強くなれます！🌳",
    "🌍「人生は旅のようなもの。楽しむことが大切だ。」- ロマン・ホリデイ。🌌\n今日も新しい発見を楽しんで、人生の旅を進めましょう！🌈",
    "🌄「毎日が新しいチャンス。」- 映画「グランド・ブダペスト・ホテル」。🌅\n新しいチャンスを掴むために、今日も最善を尽くしましょう！💪"
    "「人は弱さを克服することで、本当の強さを知る。」💪 - アーノルド・シュワルツェネッガー。\n今日の困難を乗り越えて🌄、自分の強さを見つけましょう！🌟",
    "「冒険は、扉の外に待っている。」🚪 - J.K. ローリング。\n新しい冒険に挑戦して⛵、今日も刺激的な一日を過ごしましょう！🌍",
    "「人生は、待っている人には何も与えない。」⏳ - バベ・ルース。\n積極的に行動し🏃‍♂️、今日もチャンスを掴みましょう！✨",
    "「人生の意味は、自分の道を見つけること。」🛤 - フリードリヒ・ニーチェ。\n自分だけの道を見つけ👣、それを歩んでいきましょう！🌲",
    "「私たちの人生は、私たちの考え方によって作られる。」💭 - マハトマ・ガンディー。\n良い考えを持ち続け🔄、今日も素晴らしい一日を！🌼",
    "「人は、自分が信じるものになる。」🌠 - ナポレオン・ヒル。\n自分の可能性を信じて💖、今日も努力しましょう！🔥",
    "「人生は短い。だから、後悔することなく生きなさい。」⏱ - ロビン・シャーマ。\n後悔しない選択をして🔍、今日も最高の一日を過ごしましょう！🎉",
    "「闘志なき者に勝利なし。」🥊 - 野口英世。\n戦う気持ちを忘れず🔥、今日も頑張りましょう！🌟",
    "「失敗から学び、成功へと進む。」📚 - マイケル・ジョーダン。\n挑戦の中で学びを見つけ🧠、前進しましょう！🚀",
    "「人間の真価は、逆境の中での振る舞いで判断される。」🌪 - オスカー・ワイルド。\nどんな困難にも立ち向かい💪、強さを示しましょう！🔥",
    "「一度燃えた火は二度と同じように燃えない。」🔥 - 宮沢賢治。\n今この瞬間の価値を大切に⌛、一日一日を大事にしましょう！🌹",
    "「私たちが持っている最高の武器は愛だ。」❤️ - マザー・テレサ。\n心の中の愛を大切にして💖、今日も優しさを持ち続けましょう！🕊",
    "「強さとは、どれだけの打撃を受けても前に進み続ける能力だ。」🥊 - ムハンマド・アリ。\n逆境を乗り越えて🌊、前進し続けましょう！🏃‍♂️",
    "「どんなに速く走っても、目的を見失えば道に迷う。」🧭 - ガンジー。\n方向性を明確にして🔍、一歩一歩進みましょう！👟",
    "「たとえば雨が、私たちの計画を狂わせるなら、雨を愛そう。」🌧 - ジョン・リノン。\n何が起こっても柔軟に対応し🌂、ポジティブに生きましょう！😄",
    "「やるかやらないかだけだ。試すという選択肢はない。」🚫 - ヨーダ (スター・ウォーズ)。\n迷わず行動に移し⚡、今日も全力で取り組みましょう！🌌",
    "「夢見ることを恐れてはならない。時間を失うことを恐れよ。」⏰ - ヴィクトル・ユーゴー。\n夢に向かって🌈、時間を大切に過ごしましょう！✨",
    "「人は経験によって成長する。」🌱 - ドラえもん。\n今日の経験を📖、明日の力に変えましょう！💪",
    "「やりたくないことでも、やることで道は開ける。」🚪 - ナポレオン・ヒル。\n困難を乗り越えて🏞、新しい扉を開きましょう！🔓",
    "「人生は本だ。読まない者には、一ページしかない。」📖 - セント・アウグスティン。\n新しいことに挑戦し🌟、人生のページを増やしましょう！📚",
    "「大事なのは、自分が何者であるかを知り、それを受け入れることだ。」❤️ - ピカチュウ。\n自分自身を認めて🔍、自信を持って進みましょう！🌈",
    "「人生は一度きり。後悔しないよう生きる。」⏱ - オードリー・ヘプバーン。\n今この瞬間を大切に💖、最高の一日を作りましょう！🎉"
    # 日本の名言
    "「七転び八起き」🔄 - 日本の諺。\n何度転んでも🍂、立ち上がる強さを持ちましょう！💪",
    "「石の上にも三年」⏳ - 日本の諺。\n辛抱強く続けることで🌱、結果がついてきます。今日も一日頑張りましょう！🔥",
    "「情熱を持って取り組めば、必ず道は開ける」❤️ - 松下幸之助。\n情熱の力を信じて🌟、今日も最善を尽くしましょう！💼",
    "「一期一会」🍵 - 茶道の教え。\n今この瞬間は⏳、二度と来ない。大切にし、最善を尽くしましょう！🌸",
    "「人は人、自分は自分」👥 - 井上雄彦。\n比べず🚫、自分らしさを信じて進みましょう！🌈",
    "「挑戦すること、それが人生だ」🚀 - 美空ひばり。\nどんな小さなことでも、挑戦の気持ちで取り組みましょう！💪",
    "「困難は、成功への道中の障害物に過ぎない」🏔 - 本田宗一郎。\n困難を乗り越えることで🌈、真の成功を掴みましょう！✨",
    "「何事も経験。それが一番の学び」📚 - 福沢諭吉。\n失敗を恐れず😱、経験を増やしましょう！🔍",
    "「目の前の小さな幸せを見失うな」🌼 - 宮崎駿。\n日常の小さな喜びを大切にし、ポジティブな気持ちで過ごしましょう！😊",
    "「人生は一度きり。後悔しないように生きよう」⏳ - 竹内まりや。\n今日も全力で、自分らしく生きましょう！💃",
    "「最も強い戦士は時間だ」⌛ - 太宰治。\n焦らず、時間を味方につけて、今日も一日を過ごしましょう！🌍",
    "「夢を形にするために、行動すること」🌠 - 安宅和恵。\n夢は行動とともに実現します。今日も一歩を踏み出しましょう！🚶",
    "「考える前に動くな。動く前に考えろ」🤔 - 柳本啓一。\n計画的に、そして果敢に挑戦しましょう！🚀",
    "「常に初心に返り、自分を磨き続けること」✨ - 坂本龍馬。\n初心を忘れず🍃、自己成長を目指しましょう！🌱",
    "「明日は明日の風が吹く」🌬 - 草野心平。\n過ぎ去ったことに囚われず、新しい一日を迎えましょう！🌅",
    "「自分を知り、他人を尊重せよ」🤝 - 徳川家康。\n自分の価値を理解し🔍、他人と共に今日も歩みましょう！🌍",
    "「志は高く、行動は地に足をつけて」🚀 - 渋沢栄一。\n大きな夢を持ちつつ🌌、現実的なアクションで今日を生きましょう！🌍",
    "「一日三省」🤔 - 孔子。\n今日の行動を反省し🔄、明日へのステップとしましょう！🌅",
    "「武士道とは、死ぬことと見つけたり」⚔ - 山本常一。\n全力で取り組み🔥、今日も自分の道を切り開きましょう！🌍",
    "「人を動かすのは言葉ではなく、行動だ」🚶 - 野口英世。\n言葉だけでなく🔊、実際の行動で示しましょう！🔍",
    "「雨降って地固まる」☔ - 日本の諺。\n困難を乗り越えることで🌈、より強くなれます。前向きに進みましょう！🚶",
    "「七十を過ぎても学び続けること」📚 - 曹洞宗の教え。\n学びは終わりません🚫。好奇心を持ち続けましょう！🔍",
    "「水に流す心」💧 - 日本の諺。\n過去のことは過去に🔙。新しい一日を清々しく迎えましょう！🌅",
    "「千里の道も一歩から」🚶 - 老子。\nどんなに長い旅も、一歩から始まります。勇気を持ってスタートしましょう！🚀",
    "「君子は豹変する、小人は致し難し」🔄 - 朱子。\n変化を恐れず🚫、進化し続けましょう！🚀",
    "「人は見た目ではなく、中身」❤️ - 与謝野晶子。\n外見だけでなく👀、内面を磨き続けましょう！🌌",
    "「山高きがゆえに雪は積もる」🏔 - 日本の諺。\n高みを目指せば🌌、困難も増えるが、それが成功への道。挑戦し続けましょう！🚀",
    "「人は人を、石は石を磨く」🤝 - 日本の諺。\n互いに支え合い🌍、高め合うことで成長しましょう！🌱",
    "「魚心あれば水心」❤️ - 日本の諺。\n相手に思いやりを持ち🌍、誠実に接しましょう！🤝",
    "「人生は箱のようなもの。入れるものが多ければ、それだけ豊か」📦 - 夏目漱石。\n多くの経験を積み🌍、人生を豊かにしましょう！🌱",
    "「志を立てるは易く、志を守るは難し」🔥 - 織田信長。\n始めることは簡単でも🌈、続けることが大切。今日も目標に向かって突き進みましょう！🚀",
    "「人生に失敗はありません、学びしかありません」📚 - 西郷隆盛。\nすべての経験から学ぶ心を持ち🌍、前進しましょう！🚀",
    "「雲をみる者は山を見ず」🏔 - 日本の諺。\n大局的な視点を持ち🌍、目の前の難しさに挫けないよう努力しましょう！💪",
    "「塵も積もれば山となる」🌱 - 日本の諺。\n小さな努力が大きな成果につながります。一歩一歩、進み続けましょう！🚀",
    "「人生五十年、下天のうちをくらぶれば、夢幻の如くなり」⏳ - 平家物語。\n人生は短い🚫。今日という日を大切に生きましょう！🌍",
    "「時は金なり」⌛ - 井伊直弼。\n貴重な時間を無駄にせず🚫、今日も最大限に活用しましょう！🚀",
    "「花は桜木、人は武士」🌸 - 伊藤博文。\n自分の立場を誇りに思い🌍、その役割を全うしましょう！🚀",
    "「知らざるは、言わざるにしかず」📚 - 伊能忠敬。\n知識や情報をしっかり身につけて🌍、言動に反映しましょう！🔍",
    "「人生の大敵は自分自身」🚫 - 吉田松陰。\n自分を乗り越えることで🌍、大きな成果を手に入れましょう！🚀",
    "「飛んで火に入る夏の虫」🔥 - 日本の諺。\n情熱を持って挑戦し🌍、自らの道を切り",
    # 雑学系
    "知ってましたか？フラミンゴはピンク色をしているのは、食べるエビ🦐やプランクトンの色素によるものなんです。毎日の食事が、私たちの健康や美しさに直結するんですね🥗。今日もバランスよく食事をしましょう🍽️！",
    "ペンギン🐧は一生のうちで一匹のパートナーを選ぶと言われています。大切な人との関係を大切に❤️、今日も素敵な一日を🌞！",
    "驚くかもしれませんが、バナナ🍌はハーブの仲間なんです。見た目や名前にとらわれず、新しい発見を楽しみましょう🔍！",
    "一滴の蜜を作るために、蜜蜂🐝は約2,000花を訪れるそうです。コツコツとした努力が大きな成果に繋がる、今日も一歩ずつ頑張りましょう🌼！",
    "知っていましたか？チョコレート🍫は心臓の健康に良いアンチオキシダントを含んでいるそう。だけど、食べ過ぎには注意❗️。バランスを取りながら、今日も楽しみましょう😊！",
    "宇宙の星✨の数は、地球上🌍の砂の粒よりも多いと言われています。無限の可能性を信じて💫、新しい一日をスタートしましょう🌅！",
    "カメレオンの舌👅は、自分の体よりも長いことをご存知ですか🦎？予想外の能力を秘めているかも。自分の中の新しい才能を見つけるため、今日も挑戦しましょう💪！",
    "コーヒー豆☕は、実は「果物」の種なんですよ🍇。予想外の事実に驚かされる日も、新しい発見の日として楽しんでみましょう🔍！",
    "クジラ🐋は海で最も大きい動物ですが、食事は小さなプランクトン🌊。大きな成功も、小さな努力の積み重ねから。今日もコツコツと頑張りましょう🌟！",
    "知ってましたか？チーターは最速で時速100km以上で走れますが🐆、20秒以上続けることはできません。短時間でも全力を尽くす、そんな一日を過ごしましょう🏃💨！",
    "ゴキブリは頭を切り取っても1週間生き続けることができるそうです🪳。逆境に負けない強さを持ち、今日も一日を乗り越えましょう💪！",
    "知ってましたか？金星🪐の1日は金星の1年よりも長いんです。時間の感じ方は相対的⏳。大切なのは、その時間をどう使うかですね。今日も有意義な時間を⌛！",
    "シーシュポスの神話をご存知ですか🏔️？永遠に岩を山に転がす彼のように、日常の繁忙も乗り越える鍛錬かもしれません。今日も頑張りましょう💪！",
    "トマト🍅は果物として分類されています。見た目や一般的な認識にとらわれず、自分の中の新しい一面を発見してみましょう🔍！",
    "チューリッヒ湖の水は、非常に清潔でそのまま飲むことができるそう🏞️。清らかな心を持ち💧、今日も純粋に生きましょう❤️！",
    "ホタルは光を放つことでパートナーを探します🌌。自分の輝きを信じ✨、今日も最高の一日を過ごしましょう🌟！",
    "モヤイ像🗿は、実は全身があることを知っていますか？見えている部分だけでは全てを知ることはできない。今日も新しい発見🔍を楽しみましょう！",
    "ハチミツ🍯は賞味期限がないと言われています。永遠の価値を持つものを見つけ、今日も宝物のような時間⌛を！",
    "太陽☀️の直径は地球🌍の約109倍もあります。大きな存在の前でも、自分の価値を見失わないように、今日も自分らしく💪！",
    "オウム🦜は人間の言葉を覚えることができますが、実は彼らは真似をしているだけで、意味は理解していないそう。言葉だけでなく、心の声💬を大切にしましょう！",
    "実はユニコーン🦄はスコットランドの国の動物なんですよ。信じられないことでも、可能性は無限大。今日も夢🌌を追い求めて頑張りましょう！",
    "バナナ🍌の「木」は、実は草🌿の仲間だそうです。見た目だけで判断せず、中身を大切にしましょう❤️！",
    "ボウリングのピン🎳は、正確には三角ではなく、菱形に配置されています。物事の角度を変えて考えることで、新しい発見🔄があるかも！",
    "ペンギン🐧は飛べない鳥として知られていますが、実は水中では「飛ぶ」ように泳ぎます。環境を変えることで、新しい能力💡を発揮できるかもしれませんね！",
    "「左巻き」のエスカルゴ🐌は非常に珍しいとされています。自分の個性を大切に、今日も自分らしく✨頑張りましょう！",
    "1つのチョコレートチップクッキー🍪には、約55カロリーが含まれているそう。少しの甘さ🍫で、今日のエネルギーをチャージ⚡しましょう！",
    "フラミンゴは、頭を下にして食事をします🦩。違う視点や姿勢で、新しい発見🔄があるかもしれませんね！",
    "キリン🦒の舌は、約45cmもあり、青紫色をしています。長い舌で、今日も新しいチャンス🌟をつかみ取りましょう！",
    "コーヒーの生豆は、実は緑色🟢をしています。成熟する過程で、美味しさを増していくのですね。今日も自分の成長🌱を楽しみましょう！",
    "ハワイ語には「アロハ」という言葉がありますが、愛や挨拶、さようならなど、さまざまな意味が込められています。一つの言葉にも、深い意味💬があることを忘れずに、今日もコミュニケーション🗣を楽しみましょう！",
    "チューリヒの動物園には、ペンギン🐧の恋愛マップ💘が存在します。愛の形は様々。今日も愛を感じながら過ごしましょう！",
    "エビ🦐の心臓は、その頭部にあります。場所は違えど、心は大切❤️。今日も心を大切に生きましょう！",
    "ハチ🐝は、人間の顔を覚える能力があるそう。今日も新しい出会い🤝を大切にしましょう！",
    "クロワッサン🥐は、実はオーストリア🇦🇹生まれ。物事の起源は意外なところにあるもの。新しい知識📚を得る楽しさを感じましょう！",
    "カタツムリ🐌は、最大25,000本の歯を持っていると言われています。小さな生き物にも驚きが😲。今日も新しい発見🔍を楽しみましょう！",
    "アボカド🥑は、実はベリーの一種です。見た目や名前だけで判断しない、今日も新しい視点👁を持ちましょう！",
    "コアラ🐨は、指を使ってグリップするのに適した特別な進化をしています。自分の特技✨を見つけ、今日も自分のペースで進みましょう！",
    "日本の国鳥は、キジ🦚と言われています。歴史や文化を思い出しながら、今日も日本の美しさ🌸を感じましょう！",
    "世界で最も深い湖、バイカル湖🌊には、1/5の淡水が集まっています。深みがあるものには価値が💎。今日も深く考え💭、行動しましょう！",
    "ヒマラヤの塩🧂は、古代の海🌊が乾燥したもの。時の流れとともに価値が増すものも。今日も経験を積み重ね、価値ある一日にしましょう！",
    "バナナ🍌は、技術的にはハーブ🌿の一種です。予想外の事実も楽しむ心で、今日も新しい発見🔍を楽しみましょう！",
    "ワニ🐊は、舌が口の底に固定されているため、口を開いても舌を動かすことはできません。自分の特長を生かして、今日も一歩を踏み出しましょう！",
    "人間の体内には、金や銀などの金属🪙も微量に存在します。私たちの中には未知の可能性が✨。今日も自分を信じて進みましょう！",
    "恐竜時代🦖には、3つの時間帯が存在していたと言われています。変わりゆく時代を感じながら、今日も歴史📜の一ページを刻みましょう！",
    "キリン🦒の舌は、紫がかった色をしており、太陽🌞の強い光から保護する役割があると言われています。自然の知恵に学び、今日も生き抜きましょう！",
    "太陽の光が地球🌍に到達するまでには、約8分15秒かかります。待つことの価値を知り、今日も辛抱強く進む勇気💪を持ちましょう！",
    "「左手🤚」の語源は、古い英語で「弱い」を意味する言葉から来ています。しかし、左利きの人は独特の視点や才能を持っていることが多い。特別な自分を認識し、今日も自信を持って進みましょう！",
    "ペンギン🐧は、一生の間に1つのパートナー💞だけを選ぶことが知られています。真実の愛の力を信じ、今日も心を開きましょう！",
    "蝶🦋の羽には、実は透明な鱗がついていることを知っていましたか？細部に宿る美しさを感じ、今日も周りの小さな幸せ🍀を見つけましょう！",
    "「ピアノ🎹」はイタリア語で「静かに」という意味。音楽の中の静けさを感じながら、今日も心の平和🕊を保ちましょう！",
    "1日に約2,000万本のメール📧が送信されています。情報の洪水の中でも、大切なものを見極める目👁を持ちましょう！",
    "ハチの女王🐝は、1日に約2,500回も産卵🥚することができます。大量のタスクにも負けず、今日も効率よく頑張りましょう！",
    "キウイフルーツ🥝は、実は中国🇨🇳が原産で「マキベリ」と呼ばれていました。変わる名前の背後には深い歴史📜が。今日も新しい学びを楽しみましょう！",
    "タコ🐙は3つの心臓❤️❤️❤️を持っています。多様な生命の不思議を感じながら、今日も驚きの中を進みましょう！",
    "宇宙🌌の星の数は、地球上🌍の全ての砂粒よりも多いと言われています。無限の可能性を感じ、今日も大きな夢💭を追い求めましょう！",
    "地球上で最も古い生物は約43億年前の微生物🦠とされています。長い時間の中の一瞬を大切に、今日も生き生きと過ごしましょう！",
    "チーター🐆は、最大で時速100km以上で走ることができますが、そのスピードを保てるのは数秒間だけ。短時間でも全力を出し切ることの大切さを感じましょう！",
    "ハワイ語には「アロハ」という言葉があり、愛💖や挨拶👋、さようなら👋など複数の意味があります。言葉の深さを感じながら、今日も人々とのつながりを大切にしましょう！",
    "キャベツ🥬とブロッコリー🥦は、同じ植物の異なる部位から育てられるものです。異なる角度からの視点の大切さを感じ、今日も新しい発見を楽しみましょう！",
    "「秒」⏳は、古代エジプトの日時計が起源とされています。時間の流れを感じながら、今日も有意義な一日を過ごしましょう！",
]


messages_night = [
    "今日一日お疲れ様でした🌟 明日も素敵な一日が訪れますように！",
    "夜は一日の終わりを締めくくります🌙 ゆっくり休んで、また明日！",
    "一日の終わりに、今日の良かった点を思い返してみてください😊",
    "心地よい夜をお過ごし下さい🌌 明日も良いことがたくさんありますように！",
    "良い夢をお見せください🌛 おやすみなさい！",
    "今日の努力は明日の成功に繋がります✨ しっかり休んで、また頑張りましょう！",
    "月明かりに照らされて、穏やかな夜になりますように🌜",
    "今日一日を振り返り、自分を褒めてあげてください👏 お疲れ様！",
    "おやすみ前に、深呼吸してリラックス🍃 心地よい眠りをお楽しみください！",
    "明日は新しい一日。期待と希望を持って眠りましょう🌅",
    "おやすみなさい🌕 夜空の星々があなたの夢を照らしますように！",
    "“夜は静かな時間、心の平和を取り戻しましょう”🌟",
    "“夜空に願い事を。星があなたの夢を叶えてくれるでしょう”✨",
    "“月明かりの下で、心を落ち着かせてください”🌛",
    "“おやすみなさい。リラックスして、深い眠りについてください”😴",
    "あなたの健康と安らぎのために、十分な睡眠をとってください🌙",
    "“今日はここまで。気を抜いて、安心して眠りましょう”😌",
    "おやすみなさい🌌 明日は新たな冒険が待っています！",
    "“夢の中でも、笑顔を忘れずに”😊",
    "“夜の静寂の中で、心の安らぎを感じてください”🌙",
    "“おやすみなさい。安心感に包まれて眠れますように”💤",
    "“あなたの夢が甘く、目覚めが爽やかでありますように”🌞",
    "明日も一日頑張るために、今はゆっくり休みましょう🛌",
    "今日の成功と失敗から学び、明日に活かしましょう🌅",
    "“心安らかに、ぐっすり眠りましょう”🌜",
    "“星空の下、心を静めて眠りましょう”🌠",
    "“おやすみなさい。夢の中でも、素敵な時間を”🌙",
    "“眠る前に、今日一日に感謝してみましょう”🙏",
    "“おやすみなさい。明日も素晴らしい一日になりますように”🌞",
    "“夜明け前が一番暗い。でも諦めずに、新しい一日を迎えましょう”🌅"
    "今日も一日お疲れ様でした。良い睡眠のためには、寝室を暗くしてください。暗闇はメラトニンの分泌を促進し、深い眠りをサポートします🌙",
    "今日も一日お疲れ様でした。寝る前のカフェインの摂取は控えましょう☕️ 深い眠りへと導きます。",
    "今日も一日お疲れ様でした。寝る前に少しストレッチをすると、体がリラックスして良い眠りが得られます🧘",
    "今日も一日お疲れ様でした。スマホやPCのブルーライトは睡眠の質を下げるので、寝る前は避けましょう📱💻",
    "今日も一日お疲れ様でした。寝る前に良いことを考えると、良い夢が見られることがあります💭",
    "今日も一日お疲れ様でした。寝る前の読書はリラックス効果があり、質の良い睡眠につながります📖",
    "今日も一日お疲れ様でした。お風呂でゆっくりと温まると、心も体もリラックスできます🛁 睡眠の質がアップしますよ。",
    "今日も一日お疲れ様でした。足を温めると、全身が暖かくなり睡眠の質が上がることがあります🧦",
    "今日も一日お疲れ様でした。深呼吸をすると、心拍数が落ち着き、リラックスできます😌",
    "今日も一日お疲れ様でした。適切な枕を選ぶことで、睡眠の質が向上します🛌 頭と首にフィットする枕を選びましょう。",
    "今日も一日お疲れ様でした。寝る前には重い食事を避け、消化に良い軽い食事を心がけましょう🍎",
    "今日も一日お疲れ様でした。ベッドは寝るためだけに使い、作業や食事をすることを避けましょう🛌",
    "今日も一日お疲れ様でした。適切な睡眠時間を確保することで、心身ともに健康に保てます⏰",
    "今日も一日お疲れ様でした。寝る前に温かい飲み物を摂ると、体がリラックスしやすくなります☕️",
    "今日も一日お疲れ様でした。アロマの香りでリラックスすることも、質の良い睡眠をサポートします🌿",
    "今日も一日お疲れ様でした。寝る前に明るい光を浴びることは避け、暗めの照明を選びましょう💡",
    "今日も一日お疲れ様でした。静かな音楽やホワイトノイズを聴くと、心地よい睡眠に導かれます🎶",
    "今日も一日お疲れ様でした。寝室の温度を適切に保ち、寒すぎず暑すぎない状態にしましょう🌡️",
    "今日も一日お疲れ様でした。寝る前に悩み事を考えるのは避け、ポジティブなことを考えましょう😊",
    "今日も一日お疲れ様でした。リラックスできる香りのアロマオイルやキャンドルを使用して、寝室を心地よくしましょう🕯️",
    "今日も一日お疲れ様でした。寝る前にマッサージをすると、筋肉がほぐれてリラックスできます💆",
    "今日も一日お疲れ様でした。心地よい寝具を選ぶことで、睡眠の質がグッとアップします🛏️",
    "今日も一日お疲れ様でした。寝る前に瞑想をすると、心が静まりやすくなります🧘‍♂️",
    "今日も一日お疲れ様でした。十分な睡眠をとることで、翌日のパフォーマンスも上がります🌞",
    "今日も一日お疲れ様でした。リネンスプレーで寝具に好きな香りをまとわせると、より良い眠りが得られます🌸",
    "寝る前の深呼吸はストレスを軽減します。😌 何回か深く息を吸って、リラックスしましょう。",
    "良い睡眠のためには寝室を暗く保ちましょう。🌙 暗い部屋ではメラトニンが効果的に分泌されます。",
    "睡眠中も脳は活動しています。🧠 良い夢を見ることでポジティブな気持ちになれますよ。",
    "適切な寝具は快適な睡眠をサポートします。🛏️ あなたに合った枕やマットレスを見つけましょう。",
    "緑茶に含まれるアミノ酸「L-テアニン」はリラックス効果があります。🍵 夜のティータイムを楽しんで。",
    "寝る前にスマホを見ると睡眠の質が下がることがあります。📱 できるだけ早くオフにしましょう。",
    "運動は睡眠の質を向上させますが、寝る直前の激しい運動は避けましょう。🏃‍♀️ 早めにエクササイズを。",
    "寝る前の瞑想やヨガは心を落ち着け、深い睡眠を促進します。🧘‍♀️ リラックスタイムを作りましょう。",
    "音楽は心を落ち着ける効果があります。🎶 ゆったりとした曲を聴いて、リラックスしましょう。",
    "睡眠は美容と健康の基本です。💤 しっかりと休んで、明日も美しく健康でいましょう。",
    "香りにはリラックス効果があります。🌿 ラベンダーやセージの香りで心地良い空間を作りましょう。",
    "十分な水分補給も睡眠の質を向上させます。💧 寝る前には軽く水分をとりましょう。",
    "日中の15分間のパワーナップは夜の睡眠の質を向上させることが研究で示されています。⏰ 短時間でも効果的です。",
    "今日一日お疲れ様でした！君の頑張りに感謝します🌟 明日も素敵な一日を！",
    "一日の終わりに、今日あった小さな幸せを思い出してみてください😊感謝の気持ちを持つと、素敵な夢が見れるかもしれません。",
    "今日も一生懸命働きましたね！お疲れ様です🌙 明日も新しい気持ちで頑張りましょう。",
    "今日もありがとうございました！あなたの笑顔に今日も癒されました😊おやすみなさい。",
    "一日の終わりに感謝の言葉を。今日のあなたは素晴らしかったです🌟",
    "今日も一日お疲れさま。今日があなたにとって良い日であったことを願っています🌙明日も素敵な日になりますように。",
    "今日一日お疲れ様でした！少しでもリラックスして、良い夢を見てください🌙",
    "一日お疲れさまでした！あなたの今日の努力、こちらも感じています。明日も頑張ってください🌟",
    "一日の終わりに、お疲れ様でした🌙 明日も一緒に頑張りましょうね。",
    "どんな一日だったかは分かりませんが、お疲れさまでした！感謝の気持ちを忘れずに😊",
    "素晴らしい一日でしたね！君の努力と笑顔に感謝しています🌸 明日も良い日になりますように。",
    "今日の一日、お疲れさまでした！感謝と共に、しっかり休んでくださいね😴 明日も頑張りましょう。",
    "今日もお疲れ様でした🌟 ゆっくり休んで、また明日元気に会いましょうね。",
    "今日一日お疲れさまでした！あなたの頑張り、こちらも感じていますよ😊 お休みなさい。",
    "あなたの努力に敬意を表して、お疲れさまでした🌙 明日も新しい一日が待っていますよ。",
    "今日も一日、お疲れ様。あなたの笑顔に感謝しています😊 おやすみなさい。",
    "今日はどんな日だった？お疲れさまでした！🌟 よい夢を。",
    "一日の終わりに、ありがとう🌙 あなたの努力と頑張り、素晴らしいです。お休みなさい。",
    "今日一日、お疲れ様でした🌙 良い夢を！",
    "感謝の気持ちと共に一日を締めくくりましょう🌟 お疲れさまでした！",
    "今日もあなたの温かい笑顔に感謝😊 お疲れさまでした。良い夢を！！",
    "あなたと一緒に過ごせた今日一日に感謝します🌼 おやすみなさい。",
    "今日のあなたの頑張り、見てましたよ！お疲れさま🌟 明日も一緒にがんばりましょう。",
    "今日も一日、お疲れさまでした😊 あなたの努力に感謝しています。",
    "今日も素敵な一日をありがとう🌟 お疲れ様でした。明日も期待していますよ。",
    "一日の終わりに感謝の気持ちを込めて。お疲れさまでした🌙 明日も良い日になりますように。",
    "今日のあなたはとても素敵でした🌟 お疲れさまでした！",
    "感謝と共に、今日一日お疲れさまでした😊 明日も新たな一日が始まりますね。おやすみなさい。",
    "明日は新しい一日、新しいチャンスです🌞 今日学んだことを活かしましょう！",
    "今日の終わりは明日のスタート🌅 明日も一日頑張りましょうね。",
    "新しい朝は新しい可能性を運んできます🌟 明日も素敵な一日を過ごしましょう。",
    "今日がどんな日であれ、明日は新しい１ページ📖 期待に満ちた一日にしましょう。",
    "今夜はしっかり休んで、明日に備えましょう🌙 新しい一日、新しい冒険が待っています。",
    "明日はあなたが今日よりもっと輝く日になりますように🌟 期待しています！",
    "今日一日お疲れさまでした！明日は新しい可能性が広がる一日です🌞 頑張りましょう！",
    "今日の努力が、明日の成功へと繋がりますように🌟 おやすみなさい。",
    "今日の終わりは、明日への新しいスタート🌅 より良い一日にしましょう。",
    "今夜はゆっくり休んで、明日に備えてください🌙 新しい一日があなたを待っています！",
    "明日は何が起こるかわかりませんが、新しい可能性に満ちています🚀 期待しましょう！",
    "今日の夜は明日のエネルギーをチャージ🔋 明日も頑張りましょう！",
    "明日もまた新しい一日。今日の経験を活かし、前進しましょう🌟",
    "今夜は良い夢を見て、明日に備えましょう🌙 新しい冒険が待っています！",
    "明日は今日よりもっと良くなりますよ🌞 信じて、一日を楽しみましょう！",
    "今日学んだことを明日に活かしましょう📘 新しい一日、新しい知識！",
    "明日もあなたが輝ける一日になりますように🌟 おやすみなさい。",
    "新しい朝が、新しい希望を運んでくるでしょう🌅 明日も素敵な一日になりますように。",
    "今日の努力は明日の成果につながります🚀 お疲れ様でした、そして明日もがんばりましょう！",
    "今日一日、お疲れ様でした。夜はリラックスの時間です。深い眠りでエネルギーをチャージしましょう。🌙✨",
    "素敵な夢が皆さんを訪れますように。おやすみなさい、そして明日も輝いてくださいね！🌟",
    "夜空の星々があなたに安らぎを運んでくれますように。良い夢を。✨",
    "静かな夜、心からリラックスして、新しい一日を迎える準備をしましょう。おやすみなさい！",
    "今日の営みをお疲れ様でした。心地よい睡眠で、明日への活力を得ましょう！🌜",
    "月明かりがあなたの夢を照らして、安らかな眠りをもたらしますように。おやすみなさい。",
    "今夜は自分を労わり、心地よい眠りにつきましょう。明日は新しい一日。期待と希望を持って眠りましょう。🌌",
    "夜は一日の終わりを意味し、新しい始まりへの扉です。ゆっくり休んで、明日に備えましょう。おやすみなさい！",
    "深い眠りが、あなたの心と体を癒してくれることでしょう。安らかな夜をお過ごし下さい。🌠",
    "寝る前に、今日一日の感謝の気持ちを忘れずに。心穏やかに、良い夢を見てくださいね。おやすみなさい。🌙",
    "良い睡眠は健康の基礎。リラックスして心地よい眠りにつきましょう。おやすみなさい。💤",
    "美しい夢を見るために、心を穏やかに保ちましょう。安らかな眠りをお楽しみください。🌙",
    "今日一日の疲れを癒す、深く安らかな睡眠を得ましょう。おやすみなさい、明日も頑張りましょう！",
    "寝る前の深呼吸で心を落ち着け、質の良い眠りへ。おやすみなさい。😴",
    "心地よい眠りのために、寝室を暗くして静かに。素敵な夢を見てくださいね。🌌",
    "今日のストレスを忘れ、夜の静けさに身を委ねましょう。素敵な夢を。🌟",
    "明日への活力をチャージするため、今夜はしっかりと休みましょう。おやすみなさい。🌜",
    "安らかな睡眠で心と体をリフレッシュ。明日も元気に過ごせるように。おやすみなさい。💫",
    "寝る前のリラックスタイムを大切に。心地良い睡眠をお楽しみください。おやすみなさい。🛌",
    "一日の終わりに、自分を労わり、リラックス。安らかな夜を過ごしましょう。おやすみなさい。💤",
    "音楽は心を癒します。🎵 リラックスできる音楽を聞いて、穏やかな気持ちで眠りにつきましょう。",
    "お気に入りのティーで一日の疲れを癒しましょう。☕ カモミールティーはリラックス効果抜群です。",
    "読書で心を落ち着けましょう。📚 お気に入りの本を少し読んで、質の良い眠りへと誘いましょう。",
    "暖かいバスタイムで一日の疲れを洗い流しましょう。🛁 アロマオイルを加えてリラックス効果をアップ。",
    "深呼吸で心を落ち着け、リラックスしましょう。🍃 新鮮な空気を吸い、清々しく眠りましょう。",
    "ヨガやストレッチで心と体をほぐしましょう。🧘‍♀️ 穏やかな気持ちで、ゆっくりと眠りにつきましょう。",
    "お部屋に緑を取り入れて、心を落ち着けましょう。🌱 小さな観葉植物もリラックス効果があります。",
    "美味しいデザートで自分へのご褒美。🍰 少しの甘さで心がほっとしましょう。",
    "暖かいライトでお部屋を照らしましょう。💡 やわらかな光が心地良い空間を作り出します。",
    "ペットと触れ合うことで心が癒されます。🐶 彼らの純粋な愛情に触れて、リラックスしましょう。",
    "夜空を見上げて、星の美しさに癒されましょう。🌟 明日も輝く一日になりますように。",
    "美しいアートや写真を見て、心を豊かにしましょう。🎨 美しいものに囲まれて眠りましょう。",
    "大切な人に感謝のメッセージを送りましょう。💌 心からのありがとうが、心を暖かくします。",
    "ぬくもりのあるブランケットで包まれましょう。🛏️ 快適な寝具で安らかな眠りにつきましょう。",
    "お気に入りのポエムや名言を読み返しましょう。📜 言葉の力で心を落ち着けましょう。",
    "キャンドルのやわらかな光と香りでリラックス。🕯️ 静かな時間を楽しんで、眠りましょう。",
    "お気に入りの映画やドラマで心を楽しませましょう。🎬 良い夢を見るために、ポジティブな内容を選びましょう。",
    "夜の散歩で新鮮な空気を吸いましょう。🌙 自然の音と香りで心をリフレッシュ。",
    "お気に入りのマッサージオイルで自分を労わりましょう。💆‍♀️ 軽いセルフケアで心地よく眠りにつきましょう。",
    "好きなアーティストの音楽を聞きながらリラックス。🎶 音楽の力で心を穏やかにしましょう。",
    "明日は新しいチャンスがやってきます。今日一日頑張った自分を褒めて、良い眠りにつきましょう🌙",
    "今日の終わりは、明日の始まり。休息を大切にし、新しい一日を迎えましょう✨",
    "今日一日の感謝を忘れずに。明日も素敵なことが待っていますよ🌸",
    "今日の努力は明日の成功につながります。夢に一歩近づくために、しっかり休んでください🚀",
    "どんな一日でも、明日はリセット。新しい気持ちで、新しい一日を迎えましょう☀️",
    "今日の苦労は明日の喜びに。心穏やかに、深い眠りを得ましょう🌌",
    "明日に備えて今夜は早く休むことをお勧めします。新しい朝があなたを待っています🌅",
    "今日の終わりに、自分にエールを！明日もあなたらしく、輝いてください🌟",
    "今日学んだことや感じたことを胸に、明日に活かしましょう。おやすみなさい🌜",
    "夜は一日の疲れを癒し、明日への活力をチャージする時間。ゆっくり休んで、明日も頑張りましょう💪",
]
