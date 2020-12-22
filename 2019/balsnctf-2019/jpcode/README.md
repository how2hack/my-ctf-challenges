# JPcode

Use only Japanese unicode to write shellcode with only 270 bytes length limitation.

Description:

```
シェルコード だいすき
I love shellcode <3
nc jpcode.balsnctf.com 19091

Download

Author: how2hack
```

Solves: 3/728

## Concept

I love to try different kind of shellcoding challenges. Thus, I try to create one for Balsn CTF.

The idea of this challenge is to overwrite the beginning of the shellcode and use `jecxz` instruction to jump back to your forged shellcode.

The first version of this challenge allows 498 bytes length and the range of the unicodes are:
* U+3040 ~ U+309F
* U+30A0 ~ U+30FF
* U+3190 ~ U+319F
* U+31F0 ~ U+31FF
* U+FF00 ~ U+FF9F (Notice that U+FF00~U+FF65 are not japanese but full-width symbols)

My first solution included some non-japanese unicode (which are the full-width symbols) and the length of my shellcode is 492 bytes. Then two of my teammates, [@tensxu](https://twitter.com/tensxu) and [@_yuawn](https://twitter.com/_yuawn), used unintended solution to solve the challenge.

[@tensxu](https://twitter.com/tensxu) uses `sub edi` instruction to move `edi` to the end of shellcode and uses `stos` instruction to create `int 0x80` with only 138 bytes!

[@_yuawn](https://twitter.com/_yuawn) uses ONLY Japanese unicode to create a solution!

I was very shocked and not satisfied with my own challenge because they didn't use the `jecxz` instruction to solve. So I make the challenge harder by giving more restriction. (However, there are still teams solve it without using `jecxz` because `sub edi` instruction is still available T_T)

## Challenge

The final version of this challenge is you are allowed to execute Japanese unicode shellcode with restrictions:
* U+3041 ~ U+3096
* U+3099 ~ U+309F
* U+30A0 ~ U+30FF
* U+3190 ~ U+319F
* U+31F0 ~ U+31FF
* U+FF66 ~ U+FF9F
* len(shellcode) <= 270

Your shellcode will look very :jp:.

### Useful gadgets

* `jecxz`
    * as `nop`
    * to jump back to earlier shellcode if `ecx = 0`
* `mov ebp, edi`
    * copy buf address
* `stos`
    * store value to register and increment the register
* `lods`
    * load value from register and increment the register
* `scas`
    * can use to increment the register
* `xchg eax, xxx`
    * swap registers' value

### Payload

* You can find my payload [here](exp.py).
    * `けしかﾑむさこかﾑむさにしざなこざこねははななしののしなしはしなしはははははははははははははののしなしはははははははははははははののこしなごにこねしししししししししけこけ㆑`
    * length = 86 (258)

* **$wag** (first blood team) uses `sub edi` to increase `edi` and create `int 0x80` behind their shellcode.
    * `㆖ヒ㆑フドﾐババプドﾊﾁ㆔㆖プぁｰバプビダﾐビフドｼﾁ㆖プぁｰバプビダﾐダﾐダバプ㆑㆖プビリ㆔フドﾒﾁフ㆔プ㆖ビレフドﾒﾁ㆔㆖プビ㆖プぃﾐぃﾐぃﾐぃﾐプフドﾒﾁ㆑ルヒビフ㆑ぐぐぐぐ`
    * length = 90 (270)

* **s0l0pwn** uses exactly my intended idea.
    * `けしいﾑぁざないﾓぁざないﾑぁざないｲぁさないｿぁさないﾗぁざないﾑぁざなぐぐぐ㆐いｼぁさしぃﾐぃﾐしなないﾋぁざしぃﾐしないﾀぁざなごぐぐぐぐぐぐぐぐぐぐぐけ㆐`
    * length = 81 (243)
    * Funny translation lol
	  ![LOL](https://i.imgur.com/2BH8Lek.png)

* **新竹沒放假QAQ** uses `eflags` to create `0x3`, then increase edi using `sub edi` and create `int 0x80` behind their shellcode.
    * `めﾊﾟダゑゔげぞ゜ゔゖガゕガガガガガガガガガげガガガガガガプゖゔげプぃｨﾟプゔプぃｨﾟプぃｨﾟプぃｨﾟププゖげガガゖプなゔなゔげプゑゕぐぐぐぐダぐぐぐぐぐぐぐぐぐぐぐぐぐぐぐぐぐぐ`
    * length = 90 (270)
